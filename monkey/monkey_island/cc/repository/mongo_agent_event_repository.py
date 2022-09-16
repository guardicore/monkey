import json
from typing import Any, Callable, Dict, Iterable, MutableMapping, Sequence, Type

from pymongo import MongoClient

from common.agent_event_serializers import (
    EVENT_TYPE_FIELD,
    AgentEventSerializerRegistry,
    JSONSerializable,
)
from common.agent_events import AbstractAgentEvent
from common.types import AgentID
from monkey_island.cc.repository import IAgentEventRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import RemovalError, RetrievalError, StorageError
from .consts import MONGO_OBJECT_ID_KEY

ENCRYPTED_PREFIX = "encrypted_"


def get_fields_to_encrypt(event: AbstractAgentEvent):
    return set(vars(AbstractAgentEvent)["__fields__"].keys()) ^ set(event.dict().keys())


def encrypt_event(
    encrypt: Callable[[bytes], bytes],
    event_data: JSONSerializable,
    fields: Iterable[str] = [],
) -> JSONSerializable:
    if not isinstance(event_data, dict):
        raise TypeError("Event encryption only supported for dict")

    for field in fields:
        event_data[ENCRYPTED_PREFIX + field] = str(
            encrypt(json.dumps(event_data[field]).encode()), "utf-8"
        )
        del event_data[field]

    return event_data


def decrypt_event(
    decrypt: Callable[[bytes], bytes], event_data: JSONSerializable
) -> JSONSerializable:
    if not isinstance(event_data, dict):
        raise TypeError("Event decryption only supported for dict")

    for field in event_data.keys():
        if field.startswith("encrypted_"):
            event_data[field[len(ENCRYPTED_PREFIX) :]] = json.loads(
                str(decrypt(event_data[field].encode()), "utf-8")
            )
            del event_data[field]

    return event_data


class MongoAgentEventRepository(IAgentEventRepository):
    """A repository for storing and retrieving events in MongoDB"""

    def __init__(
        self,
        mongo_client: MongoClient,
        serializer_registry: AgentEventSerializerRegistry,
        encryptor: ILockableEncryptor,
    ):
        self._events_collection = mongo_client.monkey_island.events
        self._serializers = serializer_registry
        self._encryptor = encryptor

    def save_event(self, event: AbstractAgentEvent):
        try:
            serializer = self._serializers[type(event)]
            serialized_event = serializer.serialize(event)
            fields = get_fields_to_encrypt(event)
            encrypted_event = encrypt_event(self._encryptor.encrypt, serialized_event, fields)
            self._events_collection.insert_one(encrypted_event)
        except Exception as err:
            raise StorageError(f"Error saving event: {err}")

    def get_events(self) -> Sequence[AbstractAgentEvent]:
        try:
            return self._query_events({})
        except Exception as err:
            raise RetrievalError(f"Error retrieving events: {err}")

    def get_events_by_type(
        self, event_type: Type[AbstractAgentEvent]
    ) -> Sequence[AbstractAgentEvent]:
        try:
            return self._query_events({EVENT_TYPE_FIELD: event_type.__name__})
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for type {event_type}: {err}")

    def get_events_by_tag(self, tag: str) -> Sequence[AbstractAgentEvent]:
        try:
            return self._query_events({"tags": {"$in": [tag]}})
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for tag {tag}: {err}")

    def get_events_by_source(self, source: AgentID) -> Sequence[AbstractAgentEvent]:
        try:
            return self._query_events({"source": str(source)})
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for source {source}: {err}")

    def reset(self):
        try:
            self._events_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")

    def _deserialize(self, mongo_record: MutableMapping[str, Any]) -> AbstractAgentEvent:
        decrypted_event = decrypt_event(self._encryptor.decrypt, mongo_record)
        event_type = mongo_record[EVENT_TYPE_FIELD]
        serializer = self._serializers[event_type]
        return serializer.deserialize(decrypted_event)

    def _query_events(self, query: Dict[Any, Any]) -> Sequence[AbstractAgentEvent]:
        serialized_events = self._events_collection.find(query, {MONGO_OBJECT_ID_KEY: False})
        return list(map(self._deserialize, serialized_events))
