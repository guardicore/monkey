from typing import Any, Callable, Sequence

from common.events import AbstractEvent
from .i_event_queue import IEventQueue
from pubsub import pub, ALL_TOPICS


class PypubsubEventQueue(IEventQueue):

    @staticmethod
    def subscribe_all(subscriber: Callable[..., Any]):
        pub.subscribe(listener=subscriber, topicName=ALL_TOPICS)

    def subscribe_types(self, types: Sequence[AbstractEvent], subscriber: Callable[..., Any]):
        """
        Subscribes a subscriber to all specifed event types

        :param types: Event types to which the subscriber should subscribe
        :param subscriber: Callable that should subscribe to events
        """

        pass

    def subscribe_tags(self, tags: Sequence[str], subscriber: Callable[..., Any]):
        """
        Subscribes a subscriber to all specified event tags

        :param tags: Event tags to which the subscriber should subscribe
        :param subscriber: Callable that should subscribe to events
        """

        pass

    def publish(self, event: AbstractEvent, data: Any):
        """
        Publishes an event with the given data

        :param event: Event to publish
        :param data: Data to pass to subscribers with the event publish
        """

        pass

