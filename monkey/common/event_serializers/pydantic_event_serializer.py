import logging
from typing import Type

from common.base_models import InfectionMonkeyBaseModel
from common.events import AbstractAgentEvent

from . import IEventSerializer, JSONSerializable

logger = logging.getLogger(__name__)


class PydanticEventSerializer(IEventSerializer):
    def __init__(self, event_class: Type[AbstractAgentEvent]):
        self._event_class = event_class

    def serialize(self, event: AbstractAgentEvent) -> JSONSerializable:
        if not issubclass(event.__class__, self._event_class):
            raise TypeError(f"Event object must be of type: {InfectionMonkeyBaseModel.__name__}")

        try:
            return event.dict()
        except AttributeError as err:
            logger.error(f"Error occured while serializing an event {event}: {err}")

        return None

    def deserialize(self, serialized_event: JSONSerializable) -> AbstractAgentEvent:
        return self._event_class.parse_obj(serialized_event)
