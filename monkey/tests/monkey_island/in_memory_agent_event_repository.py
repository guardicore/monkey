from typing import Sequence, Type, TypeVar

from monkeytypes import AgentID

from common.agent_events import AbstractAgentEvent
from monkey_island.cc.repositories import IAgentEventRepository

T = TypeVar("T", bound=AbstractAgentEvent)


class InMemoryAgentEventRepository(IAgentEventRepository):
    def __init__(self):
        self._events = []

    def save_event(self, event: AbstractAgentEvent):
        self._events.append(event)

    def get_events(self) -> Sequence[AbstractAgentEvent]:
        return self._events

    def get_events_by_type(self, event_type: Type[T]) -> Sequence[T]:
        type_events = []
        for event in self._events:
            if isinstance(event, event_type):
                type_events.append(event)

        return type_events

    def get_events_by_tag(self, tag: str) -> Sequence[AbstractAgentEvent]:
        pass

    def get_events_by_source(self, source: AgentID) -> Sequence[AbstractAgentEvent]:
        pass

    def reset(self):
        self._events = []
