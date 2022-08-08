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
            # pypubsub.pub.subscribe needs a string as the topic/event name
            event_type_name = event_type.__name__
            pub.subscribe(listener=subscriber, topicName=event_type_name)

    @staticmethod
    def subscribe_tags(tags: Sequence[str], subscriber: Callable[..., Any]):
        for tag in tags:
            pub.subscribe(listener=subscriber, topicName=tag)

    @staticmethod
    def publish(event: AbstractEvent, data: Any):
        # publish to event type's topic
        event_type_name = event.__name__
        pub.sendMessage(event_type_name, data)

        # publish to tags' topics
        for tag in event.tags:
            pub.sendMessage(tag, data)
