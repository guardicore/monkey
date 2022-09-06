import logging
from typing import Type

from pubsub.core import Publisher

from common.events import AbstractAgentEvent

from . import AgentEventSubscriber, IAgentEventQueue

_ALL_EVENTS_TOPIC = "all_events_topic"

logger = logging.getLogger(__name__)


class PyPubSubAgentEventQueue(IAgentEventQueue):
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher = pypubsub_publisher
        self._refs = []

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
        try:
            subscriber_name = subscriber.__name__
        except AttributeError:
            subscriber_name = subscriber.__class__.__name__

        logging.debug(f"Subscriber {subscriber_name} subscribed to {topic}")
        self._pypubsub_publisher.subscribe(topicName=topic, listener=subscriber)
        self._keep_subscriber_strongref(subscriber)

    def _keep_subscriber_strongref(self, subscriber: AgentEventSubscriber):
        # NOTE: PyPubSub stores subscribers by weak reference. From the documentation:
        #           > PyPubSub holds listeners by weak reference so that the lifetime of the
        #           > callable is not affected by PyPubSub: once the application no longer
        #           > references the callable, it can be garbage collected and PyPubSub can clean up
        #           > so it is no longer registered (this happens thanks to the weakref module).
        #           > Without this, it would be imperative to remember to unsubscribe certain
        #           > listeners, which is error prone; they would end up living until the
        #           > application exited.
        #
        #           https://pypubsub.readthedocs.io/en/v4.0.3/usage/usage_basic_tasks.html?#callable
        #
        #       In our case, we're OK with subscribers living until the application exits. We don't
        #       provide an unsubscribe method (at this time) as subscriptions are expected to last
        #       for the life of the process.
        #
        #       Specifically, if an instance object of a callable class is created and subscribed,
        #       we don't want that subscription to end if the callable instance object goes out of
        #       scope. Adding subscribers to self._refs prevents them from ever going out of scope.
        self._refs.append(subscriber)

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
        self._pypubsub_publisher.sendMessage(topic, event=event)

    # Appending a unique string to the topics for type and tags prevents bugs caused by collisions
    # between type names and tag names.
    @staticmethod
    def _get_type_topic(event_type: Type[AbstractAgentEvent]) -> str:
        return f"{event_type.__name__}-type"

    @staticmethod
    def _get_tag_topic(tag: str) -> str:
        return f"{tag}-tag"
