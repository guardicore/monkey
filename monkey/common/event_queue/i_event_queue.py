from abc import ABC, abstractmethod
from typing import Callable

from common.events import AbstractEvent


class IEventQueue(ABC):
    """
    Manages subscription and publishing of events
    """

    @abstractmethod
    def subscribe_all_events(self, subscriber: Callable[[AbstractEvent], None]):
        """
        Subscribes a subscriber to all events

        :param subscriber: Callable that should subscribe to events
        """

        pass

    @abstractmethod
    def subscribe_type(
        self, event_type: AbstractEvent, subscriber: Callable[[AbstractEvent], None]
    ):
        """
        Subscribes a subscriber to the specifed event type

        :param event_type: Event type to which the subscriber should subscribe
        :param subscriber: Callable that should subscribe to events
        """

        pass

    @abstractmethod
    def subscribe_tag(self, tag: str, subscriber: Callable[[AbstractEvent], None]):
        """
        Subscribes a subscriber to the specified event tag

        :param tag: Event tag to which the subscriber should subscribe
        :param subscriber: Callable that should subscribe to events
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
