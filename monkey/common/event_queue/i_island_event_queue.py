from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable


class IslandEventTopic(Enum):
    AGENT_CONNECTED = "agent_connected"
    CLEAR_SIMULATION_DATA = "clear_simulation_data"
    RESET_AGENT_CONFIGURATION = "reset_agent_configuration"


class IIslandEventQueue(ABC):
    """
    Manages subscription and publishing of events in the Island
    """

    @abstractmethod
    def subscribe(self, topic: IslandEventTopic, subscriber: Callable[..., None]):
        """
        Subscribes a subscriber to the specified event topic

        :param topic: Event topic to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def publish(self, topic: IslandEventTopic, event_data: Any = None):
        """
        Publishes an event topic with the given data

        :param topic: Event topic to publish
        :param event_data: Event data to pass to subscribers with the event publish
        """

        pass
