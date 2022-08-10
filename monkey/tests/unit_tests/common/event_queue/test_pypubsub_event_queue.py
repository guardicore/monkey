from dataclasses import dataclass

import pytest
from pubsub import pub

from common.event_queue.pypubsub_event_queue import (
    INTERNAL_ALL_EVENT_TYPES_TOPIC,
    PyPubSubEventQueue,
)
from common.events import AbstractEvent

EVENT_TAG_1 = "event tag 1"
EVENT_TAG_2 = "event tag 2"


@dataclass(frozen=True)
class EventType(AbstractEvent):
    source = "1234"
    target = None
    timestamp = 0.0
    tags = [EVENT_TAG_1, EVENT_TAG_2]


pypubsub_event_queue = PyPubSubEventQueue(pub)

subscriber_1_calls = subscriber_2_calls = subscriber_1 = subscriber_2 = None


@pytest.fixture(autouse=True, scope="function")
def reset_subscribers():
    global subscriber_1, subscriber_2, subscriber_1_calls, subscriber_2_calls
    subscriber_1_calls = []
    subscriber_2_calls = []
    subscriber_1 = lambda event, topic=pub.AUTO_TOPIC: subscriber_1_calls.append(topic.getName())
    subscriber_2 = lambda event, topic=pub.AUTO_TOPIC: subscriber_2_calls.append(topic.getName())


def test_topic_subscription():
    pypubsub_event_queue.subscribe_type(EventType, subscriber_1)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_2, subscriber_1)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_1, subscriber_2)
    pypubsub_event_queue.publish(EventType)

    assert subscriber_1_calls == [EventType.__name__, EVENT_TAG_2]
    assert subscriber_2_calls == [EVENT_TAG_1]


def test_subscribe_all():
    subscriber_calls = []
    subscriber = lambda topic=pub.AUTO_TOPIC: subscriber_calls.append(topic.getName())

    pypubsub_event_queue.subscribe_all(subscriber)
    pypubsub_event_queue.publish(EventType)

    assert subscriber_calls == [
        EventType.__name__,
        INTERNAL_ALL_EVENT_TYPES_TOPIC,
        EVENT_TAG_1,
        EVENT_TAG_2,
    ]


def test_subscribe_types():
    pypubsub_event_queue.subscribe_type(EventType, subscriber_1)
    pypubsub_event_queue.publish(EventType)

    assert subscriber_1_calls == [EventType.__name__]
    assert subscriber_2_calls == []


def test_subscribe_tags():
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_1, subscriber_1)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_2, subscriber_2)
    pypubsub_event_queue.publish(EventType)

    assert subscriber_1_calls == [EVENT_TAG_1]
    assert subscriber_2_calls == [EVENT_TAG_2]
