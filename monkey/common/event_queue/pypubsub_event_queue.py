from typing import Any, Callable

from common.events import AbstractEvent

from .i_event_queue import IEventQueue


class PyPubSubEventQueue(IEventQueue):
    def __init__(self, pypubsub_publisher):
        self._pypubsub_publisher = pypubsub_publisher

    def subscribe_all(self, subscriber: Callable[[AbstractEvent], None]):
        self._pypubsub_publisher.subscribe(
            listener=subscriber, topicName=self._pypubsub_publisher.ALL_TOPICS
        )

    def subscribe_type(
        self, event_type: AbstractEvent, subscriber: Callable[[AbstractEvent], None]
    ):
        # pypubsub.pub.subscribe needs a string as the topic/event name
        event_type_name = event_type.__name__
        self._pypubsub_publisher.subscribe(listener=subscriber, topicName=event_type_name)

    def subscribe_tag(self, tag: str, subscriber: Callable[[AbstractEvent], None]):
        self._pypubsub_publisher.subscribe(listener=subscriber, topicName=tag)

    def publish(self, event: AbstractEvent, data: Any = None):
        data = data if data else {}

        # publish to event type's topic
        event_type_name = event.__name__
        self._pypubsub_publisher.sendMessage(event_type_name, **data)

        # publish to tags' topics
        for tag in event.tags:
            self._pypubsub_publisher.sendMessage(tag, **data)
