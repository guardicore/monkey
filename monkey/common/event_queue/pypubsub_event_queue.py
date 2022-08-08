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
        # someClass.mro() returns a list of types that someClass is derived from,
        # in order of resolution
        # we can be sure that for any valid event, the last three items in the list will be
        # <class '__main__.AbstractEvent'>, <class 'abc.ABC'>, and <class 'object'>

        # for some event, say, CredentialsStolenEvent which was derived from SecurityEvent,
        # we want to publish the data to both events, so, we loop through the super
        # classes of the CredentialsStolenEvent which was initially passed as an argument
        # to the function, and publish to each class's type and tags (except the last 3 classes)
        for event_type in event.mro()[:-3]:
            PypubsubEventQueue._publish_to_type(event_type, data)
            PypubsubEventQueue._publish_to_tags(event_type, data)

    @staticmethod
    def _publish_to_type(event_type: AbstractEvent, data: Any):
        event_type_name = event_type.__name__
        pub.sendMessage(event_type_name, data)

    @staticmethod
    def _publish_to_tags(event_type: AbstractEvent, data: Any):
        for tag in event_type.tags:
            pub.sendMessage(tag, data)
