from typing import Any, MutableMapping, Sequence, Type

from pymongo import MongoClient

from common.event_serializers import EVENT_TYPE_FIELD, EventSerializerRegistry
from common.events import AbstractAgentEvent
from common.types import AgentID
from monkey_island.cc.repository import IEventRepository

from . import RemovalError, RetrievalError, StorageError
from .consts import MONGO_OBJECT_ID_KEY


class MongoEventRepository(IEventRepository):
    def __init__(self, mongo_client: MongoClient, serializer_registry: EventSerializerRegistry):
        self._events_collection = mongo_client.monkey_island.events
        self._serializers = serializer_registry

    def save_event(self, event: AbstractAgentEvent):
        try:
            serializer = self._serializers[type(event)]
            serialized_event = serializer.serialize(event)
            self._events_collection.insert_one(serialized_event)
        except Exception as err:
            raise StorageError(err)

    def get_events(self) -> Sequence[AbstractAgentEvent]:
        try:
            serialized_events = list(self._events_collection.find())
            return list(map(self._deserialize, serialized_events))
        except Exception as err:
            raise RetrievalError(f"Error retrieving events: {err}")

    def get_events_by_type(
        self, event_type: Type[AbstractAgentEvent]
    ) -> Sequence[AbstractAgentEvent]:
        try:
            serialized_events = list(
                self._events_collection.find({EVENT_TYPE_FIELD: event_type.__name__})
            )
            return list(map(self._deserialize, serialized_events))
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for type {event_type}: {err}")

    def get_events_by_tag(self, tag: str) -> Sequence[AbstractAgentEvent]:
        try:
            serialized_events = list(self._events_collection.find({"tags": {"$in": [tag]}}))
            return list(map(self._deserialize, serialized_events))
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for tag {tag}: {err}")

    def get_events_by_source(self, source: AgentID) -> Sequence[AbstractAgentEvent]:
        try:
            serialized_events = list(self._events_collection.find({"source": source}))
            return list(map(self._deserialize, serialized_events))
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for source {source}: {err}")

    def reset(self):
        try:
            self._events_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")

    def _deserialize(self, mongo_record: MutableMapping[str, Any]) -> AbstractAgentEvent:
        del mongo_record[MONGO_OBJECT_ID_KEY]
        event_type = mongo_record[EVENT_TYPE_FIELD]
        serializer = self._serializers[event_type]
        return serializer.deserialize(mongo_record)
