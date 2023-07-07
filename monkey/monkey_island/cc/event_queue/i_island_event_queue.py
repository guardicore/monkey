from abc import ABC, abstractmethod
from enum import Enum, auto

from . import IslandEventSubscriber


class IslandEventTopic(Enum):
    AGENT_HEARTBEAT = auto()
    AGENT_REGISTERED = auto()
    AGENT_TIMED_OUT = auto()
    CLEAR_SIMULATION_DATA = auto()
    RESET_AGENT_CONFIGURATION = auto()
    TERMINATE_AGENTS = auto()


class IIslandEventQueue(ABC):
    """
    Manages subscription and publishing of events in the Island
    """

    @abstractmethod
    def subscribe(self, topic: IslandEventTopic, subscriber: IslandEventSubscriber):
        """
        Subscribes a subscriber to the specified event topic

        :param topic: Event topic to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def publish(self, topic: IslandEventTopic, **kwargs):
        """
        Publishes an event topic with the given data

        :param topic: Event topic to publish
        :param **kwargs: Event data to publish
        """

        pass
