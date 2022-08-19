import logging
from typing import Type

from pubsub.core import Publisher

from common.events import AbstractEvent

from . import EventSubscriber, IEventQueue

_ALL_EVENTS_TOPIC = "all_events_topic"

logger = logging.getLogger(__name__)


class PyPubSubEventQueue(IEventQueue):
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher = pypubsub_publisher

    def subscribe_all_events(self, subscriber: EventSubscriber):
        self._subscribe(_ALL_EVENTS_TOPIC, subscriber)

    def subscribe_type(self, event_type: Type[AbstractEvent], subscriber: EventSubscriber):
        # pypubsub.pub.subscribe needs a string as the topic/event name
        event_type_topic = PyPubSubEventQueue._get_type_topic(event_type)
        self._subscribe(event_type_topic, subscriber)

    def subscribe_tag(self, tag: str, subscriber: EventSubscriber):
        tag_topic = PyPubSubEventQueue._get_tag_topic(tag)
        self._subscribe(tag_topic, subscriber)

    def _subscribe(self, topic: str, subscriber: EventSubscriber):
        try:
            subscriber_name = subscriber.__name__
        except AttributeError:
            subscriber_name = subscriber.__class__.__name__

        logging.debug(f"Subscriber {subscriber_name} subscribed to {topic}")
        self._pypubsub_publisher.subscribe(topicName=topic, listener=subscriber)

    def publish(self, event: AbstractEvent):
        self._publish_to_all_events_topic(event)
        self._publish_to_type_topic(event)
        self._publish_to_tags_topics(event)

    def _publish_to_all_events_topic(self, event: AbstractEvent):
        self._publish_event(_ALL_EVENTS_TOPIC, event)

    def _publish_to_type_topic(self, event: AbstractEvent):
        event_type_topic = PyPubSubEventQueue._get_type_topic(event.__class__)
        self._publish_event(event_type_topic, event)

    def _publish_to_tags_topics(self, event: AbstractEvent):
        for tag in event.tags:
            tag_topic = PyPubSubEventQueue._get_tag_topic(tag)
            self._publish_event(tag_topic, event)

    def _publish_event(self, topic: str, event: AbstractEvent):
        logger.debug(f"Publishing a {event.__class__.__name__} event to {topic}")
        self._pypubsub_publisher.sendMessage(topic, event=event)

    # Appending a unique string to the topics for type and tags prevents bugs caused by collisions
    # between type names and tag names.
    @staticmethod
    def _get_type_topic(event_type: Type[AbstractEvent]) -> str:
        return f"{event_type.__name__}-type"

    @staticmethod
    def _get_tag_topic(tag: str) -> str:
        return f"{tag}-tag"
