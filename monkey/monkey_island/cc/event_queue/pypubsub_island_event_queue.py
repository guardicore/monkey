import logging
from typing import Any

from pubsub.core import Publisher

from common.event_queue import PyPubSubPublisherWrapper

from . import IIslandEventQueue, IslandEventSubscriber, IslandEventTopic

logger = logging.getLogger(__name__)


class PyPubSubIslandEventQueue(IIslandEventQueue):
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher_wrapped = PyPubSubPublisherWrapper(pypubsub_publisher)

    def subscribe(self, topic: IslandEventTopic, subscriber: IslandEventSubscriber):
        topic_name = topic.name  # needs to be a string for pypubsub

        # NOTE: The subscriber's signature needs to match the MDS (message data specification) of
        #       the topic, otherwise, errors will arise. The MDS of a topic is set when the topic
        #       is created, which in our case is when a subscriber subscribes to a topic which
        #       is new (hasn't been subscribed to before). If the topic is being subscribed to by
        #       a subscriber for the first time, the topic's MDS will automatically be set
        #       according to that subscriber's signature.
        self._pypubsub_publisher_wrapped.subscribe(topic_name, subscriber)

    def publish(self, topic: IslandEventTopic, event: Any = None):
        topic_name = topic.name  # needs to be a string for pypubsub

        logger.debug(f"Publishing {topic_name} event")

        # NOTE: `event_data` needs to match the MDS (message data specification) of the topic,
        #       otherwise, errors will arise. The MDS of a topic is set when the topic is created,
        #       which in our case is when a subscriber subscribes to a topic (in `subscribe()`)
        #       which is new (hasn't been subscribed to before).
        self._pypubsub_publisher_wrapped.publish(topic_name, event)
