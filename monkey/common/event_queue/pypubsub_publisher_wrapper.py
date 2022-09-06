import logging
from typing import Any, Callable

from pubsub.core import Publisher

logger = logging.getLogger(__name__)


class PyPubSubPublisherWrapper:
    def __init__(self, pypubsub_publisher: Publisher):
        self._pypubsub_publisher = pypubsub_publisher
        self._refs = []

    def subscribe(self, topic_name: str, subscriber: Callable):
        try:
            subscriber_name = subscriber.__name__
        except AttributeError:
            subscriber_name = subscriber.__class__.__name__

        logging.debug(f"Subscriber {subscriber_name} subscribed to {topic_name}")

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

    def publish(self, topic_name: str, event: Any = None):
        self._pypubsub_publisher.sendMessage(topicName=topic_name, event=event)
