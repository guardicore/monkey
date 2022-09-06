from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable


class IslandEventTopics(Enum):
    AGENT_CONNECTED = auto()
    CLEAR_SIMULATION_DATA = auto()
    RESET_AGENT_CONFIGURATION = auto()


class IIslandEventQueue(ABC):
    """
    Manages subscription and publishing of events in the Island
    """

    @abstractmethod
    def subscribe(self, topic: IslandEventTopics, subscriber: Callable[..., None]):
        """
        Subscribes a subscriber to the specified event topic

        :param topic: Event topic to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def publish(self, topic: IslandEventTopics, event_data: Any = None):
        """
        Publishes an event topic with the given data

        :param topic: Event topic to publish
        :param event_data: Event data to pass to subscribers with the event publish
        """

        pass
