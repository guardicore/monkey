import logging
from typing import Type

from monkeyevents import AbstractAgentEvent
from pubsub.core import Publisher

from common.event_queue import PyPubSubPublisherWrapper

from . import AgentEventSubscriber, IAgentEventQueue

_ALL_EVENTS_TOPIC = "all_events_topic"

logger = logging.getLogger(__name__)


class PyPubSubAgentEventQueue(IAgentEventQueue):
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher_wrapper = PyPubSubPublisherWrapper(pypubsub_publisher)

    def subscribe_all_events(self, subscriber: AgentEventSubscriber):
        self._subscribe(_ALL_EVENTS_TOPIC, subscriber)

    def subscribe_type(
        self, event_type: Type[AbstractAgentEvent], subscriber: AgentEventSubscriber
    ):
        # pypubsub.pub.subscribe needs a string as the topic/event name
        event_type_topic = PyPubSubAgentEventQueue._get_type_topic(event_type)
        self._subscribe(event_type_topic, subscriber)

    def subscribe_tag(self, tag: str, subscriber: AgentEventSubscriber):
        tag_topic = PyPubSubAgentEventQueue._get_tag_topic(tag)
        self._subscribe(tag_topic, subscriber)

    def _subscribe(self, topic: str, subscriber: AgentEventSubscriber):
        self._pypubsub_publisher_wrapper.subscribe(topic, subscriber)

    def publish(self, event: AbstractAgentEvent):
        self._publish_to_all_events_topic(event)
        self._publish_to_type_topic(event)
        self._publish_to_tags_topics(event)

    def _publish_to_all_events_topic(self, event: AbstractAgentEvent):
        self._publish_event(_ALL_EVENTS_TOPIC, event)

    def _publish_to_type_topic(self, event: AbstractAgentEvent):
        event_type_topic = PyPubSubAgentEventQueue._get_type_topic(event.__class__)
        self._publish_event(event_type_topic, event)

    def _publish_to_tags_topics(self, event: AbstractAgentEvent):
        for tag in event.tags:
            tag_topic = PyPubSubAgentEventQueue._get_tag_topic(tag)
            self._publish_event(tag_topic, event)

    def _publish_event(self, topic: str, event: AbstractAgentEvent):
        logger.debug(f"Publishing a {event.__class__.__name__} event to {topic}")
        self._pypubsub_publisher_wrapper.publish(topic, event=event)

    # Appending a unique string to the topics for type and tags prevents bugs caused by collisions
    # between type names and tag names.
    @staticmethod
    def _get_type_topic(event_type: Type[AbstractAgentEvent]) -> str:
        return f"{event_type.__name__}-type"

    @staticmethod
    def _get_tag_topic(tag: str) -> str:
        return f"{tag}-tag"
