from typing import Any, Dict, Sequence, Type

from pymongo import MongoClient

from common.agent_event_serializers import EVENT_TYPE_FIELD, AgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent
from common.types import AgentID
from monkey_island.cc.repository import IAgentEventRepository
from monkey_island.cc.repository.i_agent_event_repository import T
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import RemovalError, RetrievalError, StorageError
from .agent_event_encryption import decrypt_event, encrypt_event
from .consts import MONGO_OBJECT_ID_KEY


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
            encrypted_event = encrypt_event(self._encryptor.encrypt, serialized_event)
            self._events_collection.insert_one(encrypted_event)
        except Exception as err:
            raise StorageError(f"Error saving event: {err}")

    def get_events(self) -> Sequence[AbstractAgentEvent]:
        try:
            return self._query_events({})
        except Exception as err:
            raise RetrievalError(f"Error retrieving events: {err}")

    def get_events_by_type(self, event_type: Type[T]) -> Sequence[T]:
        try:
            return self._query_events({EVENT_TYPE_FIELD: event_type.__name__})  # type: ignore[return-value]  # noqa: E501
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

    def _deserialize(self, mongo_record: Dict[str, Any]) -> AbstractAgentEvent:
        decrypted_event = decrypt_event(self._encryptor.decrypt, mongo_record)
        event_type = mongo_record[EVENT_TYPE_FIELD]
        serializer = self._serializers[event_type]
        return serializer.deserialize(decrypted_event)

    def _query_events(self, query: Dict[Any, Any]) -> Sequence[AbstractAgentEvent]:
        serialized_events = self._events_collection.find(query, {MONGO_OBJECT_ID_KEY: False})
        return list(map(self._deserialize, serialized_events))
