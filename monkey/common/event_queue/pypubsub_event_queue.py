from typing import Any, Callable

from pubsub import pub

from common.events import AbstractEvent

from .i_event_queue import IEventQueue


class PyPubSubEventQueue(IEventQueue):
    @staticmethod
    def subscribe_all(subscriber: Callable[[AbstractEvent], None]):
        pub.subscribe(listener=subscriber, topicName=pub.ALL_TOPICS)

    @staticmethod
    def subscribe_type(event_type: AbstractEvent, subscriber: Callable[[AbstractEvent], None]):
        # pypubsub.pub.subscribe needs a string as the topic/event name
        event_type_name = event_type.__name__
        pub.subscribe(listener=subscriber, topicName=event_type_name)

    @staticmethod
    def subscribe_tag(tag: str, subscriber: Callable[[AbstractEvent], None]):
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
