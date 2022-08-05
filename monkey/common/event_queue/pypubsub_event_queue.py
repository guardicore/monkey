from typing import Any, Callable, Sequence

from pubsub import ALL_TOPICS, pub

from common.events import AbstractEvent

from .i_event_queue import IEventQueue


class PypubsubEventQueue(IEventQueue):
    @staticmethod
    def subscribe_all(subscriber: Callable[..., Any]):
        pub.subscribe(listener=subscriber, topicName=ALL_TOPICS)

    @staticmethod
    def subscribe_types(types: Sequence[AbstractEvent], subscriber: Callable[..., Any]):
        for event_type in types:
            PypubsubEventQueue._subscribe_type(event_type, subscriber)

    def _subscribe_type(event_type: AbstractEvent, subscriber: Callable[..., Any]):
        event_type_name = event_type.__name__
        pub.subscribe(subscriber, event_type_name)

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
