from abc import ABC, abstractmethod
from typing import Dict, List, Union

from common.events import AbstractAgentEvent

JSONSerializable = Union[
    Dict[str, "JSONSerializable"], List["JSONSerializable"], int, str, float, bool, None
]


class IEventSerializer(ABC):
    """
    Manages serialization and deserialization of events
    """

    @abstractmethod
    def serialize(self, event: AbstractAgentEvent) -> JSONSerializable:
        """
        Serializes an event

        :param event: Event to serialize
        :return: Serialized event
        """
        pass

    @abstractmethod
    def deserialize(self, serialized_event: JSONSerializable) -> AbstractAgentEvent:
        """
        Deserializes an event

        :param serialized_event: Serialized event to deserialize
        :return: Deserialized event
        """
        pass
