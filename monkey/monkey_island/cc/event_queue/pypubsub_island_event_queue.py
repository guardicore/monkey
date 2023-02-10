import logging

from pubsub.core import Publisher

from common.event_queue import PyPubSubPublisherWrapper

from . import IIslandEventQueue, IslandEventSubscriber, IslandEventTopic

logger = logging.getLogger(__name__)


class PyPubSubIslandEventQueue(IIslandEventQueue):
    """
    Implements IIslandEventQueue using pypubsub
    """

    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher_wrapper = PyPubSubPublisherWrapper(pypubsub_publisher)

    def subscribe(self, topic: IslandEventTopic, subscriber: IslandEventSubscriber):
        topic_name = topic.name  # needs to be a string for pypubsub
        self._pypubsub_publisher_wrapper.subscribe(topic_name, subscriber)

    def publish(self, topic: IslandEventTopic, **kwargs):
        topic_name = topic.name  # needs to be a string for pypubsub
        logger.debug(f"Publishing {topic_name} event")

        self._pypubsub_publisher_wrapper.publish(topic_name, **kwargs)
