import logging
from typing import Generic, Type, TypeVar

from common.agent_events import AbstractAgentEvent
from common.types import JSONSerializable

from . import EVENT_TYPE_FIELD, IAgentEventSerializer

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=AbstractAgentEvent)


class PydanticAgentEventSerializer(IAgentEventSerializer, Generic[T]):
    def __init__(self, event_class: Type[T]):
        self._event_class = event_class

    def serialize(self, event: T) -> JSONSerializable:
        if not isinstance(event, self._event_class):
            raise TypeError(f"Event object must be of type: {self._event_class.__name__}")

        event_dict = event.dict(simplify=True)
        event_dict[EVENT_TYPE_FIELD] = type(event).__name__

        return event_dict

    def deserialize(self, serialized_event: JSONSerializable) -> T:
        if not isinstance(serialized_event, dict):
            raise TypeError(
                "Serialized pydantic events must be a dictionary, but got {type(serialized_event)}"
            )

        # pydantic serialized events will always be dicts with a copy() method
        event_dict = serialized_event.copy()  # type: ignore[union-attr]
        event_dict.pop(EVENT_TYPE_FIELD, None)

        return self._event_class(**event_dict)
