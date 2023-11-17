from abc import ABC, abstractmethod
from typing import Type

from monkeyevents import AbstractAgentEvent

from . import AgentEventSubscriber


class IAgentEventQueue(ABC):
    """
    Manages subscription and publishing of events in the Agent
    """

    @abstractmethod
    def subscribe_all_events(self, subscriber: AgentEventSubscriber):
        """
        Subscribes a subscriber to all events

        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def subscribe_type(
        self, event_type: Type[AbstractAgentEvent], subscriber: AgentEventSubscriber
    ):
        """
        Subscribes a subscriber to the specified event type

        :param event_type: Event type to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def subscribe_tag(self, tag: str, subscriber: AgentEventSubscriber):
        """
        Subscribes a subscriber to the specified event tag

        :param tag: Event tag to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def publish(self, event: AbstractAgentEvent):
        """
        Publishes an event with the given data

        :param event: Event to publish
        """

        pass
