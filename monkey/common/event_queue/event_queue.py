from typing import Any, Callable, Sequence

from pubsub import pub

from common.events import AbstractEvent

from .i_event_queue import IEventQueue


class EventQueue(IEventQueue):
    @staticmethod
    def subscribe_all(subscriber: Callable[..., Any]):
        pub.subscribe(listener=subscriber, topicName=pub.ALL_TOPICS)

    @staticmethod
    def subscribe_types(types: Sequence[AbstractEvent], subscriber: Callable[..., Any]):
        for event_type in types:
            # pypubsub.pub.subscribe needs a string as the topic/event name
            event_type_name = event_type.__name__
            pub.subscribe(listener=subscriber, topicName=event_type_name)

    @staticmethod
    def subscribe_tags(tags: Sequence[str], subscriber: Callable[..., Any]):
        for tag in tags:
            pub.subscribe(listener=subscriber, topicName=tag)

    @staticmethod
    def publish(event: AbstractEvent, data: Any = None):
        data = data if data else {}

        # publish to event type's topic
        event_type_name = event.__name__
        pub.sendMessage(event_type_name, **data)

        # publish to tags' topics
        for tag in event.tags:
            pub.sendMessage(tag, **data)

    @staticmethod
    def unsubscribe_all(subscriber: Callable[..., Any]):
        pub.unsubscribe(listener=subscriber, topicName=pub.ALL_TOPICS)

    @staticmethod
    def unsubscribe_types(types: Sequence[AbstractEvent], subscriber: Callable[..., Any]):
        for event_type in types:
            # pypubsub.pub.subscribe needs a string as the topic/event name
            event_type_name = event_type.__name__
            pub.unsubscribe(listener=subscriber, topicName=event_type_name)

    @staticmethod
    def unsubscribe_tags(tags: Sequence[str], subscriber: Callable[..., Any]):
        for tag in tags:
            pub.unsubscribe(listener=subscriber, topicName=tag)
