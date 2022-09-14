from typing import Sequence, Type

from pymongo import MongoClient

from common.events import AbstractAgentEvent
from common.types import AgentID
from monkey_island.cc.repository import IEventRepository

from . import RemovalError, RetrievalError, StorageError


class MongoEventRepository(IEventRepository):
    def __init__(self, mongo_client: MongoClient):
        self._events_collection = mongo_client.monkey_island.events

    def save_event(self, event: AbstractAgentEvent):
        try:
            self._events_collection.insert_one(event.dict(simplify=True))
        except Exception as err:
            raise StorageError(err)

    def get_events(self) -> Sequence[AbstractAgentEvent]:
        try:
            return list(self._events_collection.find())
        except Exception as err:
            raise RetrievalError(f"Error retrieving events: {err}")

    def get_events_by_type(
        self, event_type: Type[AbstractAgentEvent]
    ) -> Sequence[AbstractAgentEvent]:
        try:
            return []
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for type {event_type}: {err}")

    def get_events_by_tag(self, tag: str) -> Sequence[AbstractAgentEvent]:
        try:
            return list(self._events_collection.find({"tags": {"$in": [tag]}}))
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for tag {tag}: {err}")

    def get_events_by_source(self, source: AgentID) -> Sequence[AbstractAgentEvent]:
        try:
            return list(self._events_collection.find({"source": source}))
        except Exception as err:
            raise RetrievalError(f"Error retrieving events for source {source}: {err}")

    def reset(self):
        try:
            self._events_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")
