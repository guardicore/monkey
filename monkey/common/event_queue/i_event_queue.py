from abc import ABC, abstractstaticmethod
from typing import Any, Callable

from common.events import AbstractEvent


class IEventQueue(ABC):
    """
    Manages subscription and publishing of events
    """

    @abstractstaticmethod
    def subscribe_all(subscriber: Callable[[AbstractEvent], None]):
        """
        Subscribes a subscriber to all events

        :param subscriber: Callable that should subscribe to events
        """

        pass

    @abstractstaticmethod
    def subscribe_type(event_type: AbstractEvent, subscriber: Callable[[AbstractEvent], None]):
        """
        Subscribes a subscriber to the specifed event type

        :param event_type: Event type to which the subscriber should subscribe
        :param subscriber: Callable that should subscribe to events
        """

        pass

    @abstractstaticmethod
    def subscribe_tag(tag: str, subscriber: Callable[[AbstractEvent], None]):
        """
        Subscribes a subscriber to the specified event tag

        :param tag: Event tag to which the subscriber should subscribe
        :param subscriber: Callable that should subscribe to events
        """

        pass

    @abstractstaticmethod
    def publish(event: AbstractEvent, data: Any):
        """
        Publishes an event with the given data

        :param event: Event to publish
        :param data: Data to pass to subscribers with the event publish
        """

        pass
