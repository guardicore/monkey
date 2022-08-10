from typing import Type

from pubsub.core import Publisher

from common.events import AbstractEvent

from . import EventSubscriber
from .i_event_queue import IEventQueue

_ALL_EVENTS_TOPIC = "all_events_topic"


class PyPubSubEventQueue(IEventQueue):
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher = pypubsub_publisher

    def subscribe_all_events(self, subscriber: EventSubscriber):
        self._pypubsub_publisher.subscribe(listener=subscriber, topicName=_ALL_EVENTS_TOPIC)

    def subscribe_type(self, event_type: Type[AbstractEvent], subscriber: EventSubscriber):
        # pypubsub.pub.subscribe needs a string as the topic/event name
        event_type_topic = PyPubSubEventQueue._get_type_topic(event_type)
        self._pypubsub_publisher.subscribe(listener=subscriber, topicName=event_type_topic)

    def subscribe_tag(self, tag: str, subscriber: EventSubscriber):
        tag_topic = PyPubSubEventQueue._get_tag_topic(tag)
        self._pypubsub_publisher.subscribe(listener=subscriber, topicName=tag_topic)

    def publish(self, event: AbstractEvent):
        self._publish_to_all_events_topic(event)
        self._publish_to_type_topic(event)
        self._publish_to_tags_topics(event)

    def _publish_to_all_events_topic(self, event: AbstractEvent):
        self._pypubsub_publisher.sendMessage(_ALL_EVENTS_TOPIC, event=event)

    def _publish_to_type_topic(self, event: AbstractEvent):
        event_type_topic = PyPubSubEventQueue._get_type_topic(event.__class__)
        self._pypubsub_publisher.sendMessage(event_type_topic, event=event)

    def _publish_to_tags_topics(self, event: AbstractEvent):
        for tag in event.tags:
            tag_topic = PyPubSubEventQueue._get_tag_topic(tag)
            self._pypubsub_publisher.sendMessage(tag_topic, event=event)

    # Appending a unique string to the topics for type and tags prevents bugs caused by collisions
    # between type names and tag names.
    @staticmethod
    def _get_type_topic(event_type: Type[AbstractEvent]) -> str:
        return f"{event_type.__name__}-type"

    @staticmethod
    def _get_tag_topic(tag: str) -> str:
        return f"{tag}-tag"
