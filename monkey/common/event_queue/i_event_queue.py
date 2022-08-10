from abc import ABC, abstractmethod
from typing import Type

from common.events import AbstractEvent

from . import EventSubscriber


class IEventQueue(ABC):
    """
    Manages subscription and publishing of events
    """

    @abstractmethod
    def subscribe_all_events(self, subscriber: EventSubscriber):
        """
        Subscribes a subscriber to all events

        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def subscribe_type(self, event_type: Type[AbstractEvent], subscriber: EventSubscriber):
        """
        Subscribes a subscriber to the specified event type

        :param event_type: Event type to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def subscribe_tag(self, tag: str, subscriber: EventSubscriber):
        """
        Subscribes a subscriber to the specified event tag

        :param tag: Event tag to which the subscriber should subscribe
        :param subscriber: A subscriber that will receive events
        """

        pass

    @abstractmethod
    def publish(self, event: AbstractEvent):
        """
        Publishes an event with the given data

        :param event: Event to publish
        :param data: Data to pass to subscribers with the event publish
        """

        pass
