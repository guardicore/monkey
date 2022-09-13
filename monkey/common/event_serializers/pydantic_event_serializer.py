import logging
from typing import Generic, Type, TypeVar

from common.events import AbstractAgentEvent

from . import IEventSerializer, JSONSerializable

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=AbstractAgentEvent)


class PydanticEventSerializer(IEventSerializer, Generic[T]):
    def __init__(self, event_class: Type[T]):
        self._event_class = event_class

    def serialize(self, event: T) -> JSONSerializable:
        if not issubclass(event.__class__, self._event_class):
            raise TypeError(f"Event object must be of type: {self._event_class.__name__}")

        try:
            return event.dict()
        except AttributeError as err:
            logger.error(f"Error occured while serializing an event {event}: {err}")

        return None

    def deserialize(self, serialized_event: JSONSerializable) -> T:
        return self._event_class(**serialized_event)
