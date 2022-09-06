from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from . import IslandEventSubscriber

IslandEventTopic = Enum(
    "IslandEventTopic", ["AGENT_CONNECTED", "CLEAR_SIMULATION_DATA", "RESET_AGENT_CONFIGURATION"]
)


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
    def publish(self, topic: IslandEventTopic, event: Any = None):
        """
        Publishes an event topic with the given data

        :param topic: Event topic to publish
        :param event: Event data to publish
        """

        pass
