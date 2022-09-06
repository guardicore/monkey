import logging
from typing import Callable, List

from pubsub.core import Publisher

logger = logging.getLogger(__name__)


class PyPubSubPublisherWrapper:
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher = pypubsub_publisher
        self._refs: List[Callable] = []

    def subscribe(self, topic_name: str, subscriber: Callable):
        try:
            subscriber_name = subscriber.__name__
        except AttributeError:
            subscriber_name = subscriber.__class__.__name__

        logging.debug(f"Subscriber {subscriber_name} subscribed to {topic_name}")

        # NOTE: The subscriber's signature needs to match the MDS (message data specification) of
        #       the topic, otherwise, errors will arise. The MDS of a topic is set when the topic
        #       is created, which in our case is when a subscriber subscribes to a topic which
        #       is new (hasn't been subscribed to before). If the topic is being subscribed to by
        #       a subscriber for the first time, the topic's MDS will automatically be set
        #       according to that subscriber's signature.
        self._pypubsub_publisher.subscribe(topicName=topic_name, listener=subscriber)
        self._keep_subscriber_strongref(subscriber)

    def _keep_subscriber_strongref(self, subscriber: Callable):
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

    def publish(self, topic_name: str, **kwargs):
        # NOTE: `kwargs` needs to match the MDS (message data specification) of the topic,
        #       otherwise, errors will arise. The MDS of a topic is set when the topic is created,
        #       which in our case is when a subscriber subscribes to a topic (in `subscribe()`)
        #       which is new (hasn't been subscribed to before).
        self._pypubsub_publisher.sendMessage(topicName=topic_name, **kwargs)
