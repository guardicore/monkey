from abc import ABC, abstractmethod

from monkeytypes import JSONSerializable

from common.agent_events import AbstractAgentEvent


class IAgentEventSerializer(ABC):
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
        :raises TypeError: If one or more of the serialized fields contains data of an incompatible
                           type
        :raises ValueError: If one or more of the serialized fields contains an incompatible value
        """
        pass
