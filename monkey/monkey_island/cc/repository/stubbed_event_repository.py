from typing import Sequence, Type, TypeVar

from common.agent_events import AbstractAgentEvent
from common.types import AgentID

from . import IAgentEventRepository

T = TypeVar("T", bound=AbstractAgentEvent)


# TODO: Remove this class after #2180 is complete
class StubbedEventRepository(IAgentEventRepository):
    def save_event(self, event: AbstractAgentEvent):
        return

    def get_events(self) -> Sequence[AbstractAgentEvent]:
        return []

    def get_events_by_type(self, event_type: Type[T]) -> Sequence[T]:
        return []

    def get_events_by_tag(self, tag: str) -> Sequence[AbstractAgentEvent]:
        return []

    def get_events_by_source(self, source: AgentID) -> Sequence[AbstractAgentEvent]:
        return []

    def reset(self):
        return
