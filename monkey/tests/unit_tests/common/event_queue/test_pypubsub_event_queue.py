from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import FrozenSet, Union
from uuid import UUID

import pytest
from pubsub import pub

from common.event_queue.pypubsub_event_queue import PyPubSubEventQueue
from common.events import AbstractEvent

EVENT_TAG_1 = "event tag 1"
EVENT_TAG_2 = "event tag 2"


@dataclass(frozen=True)
class TestEvent(AbstractEvent):
    source: UUID = "f811ad00-5a68-4437-bd51-7b5cc1768ad5"
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet = frozenset()


pypubsub_event_queue = PyPubSubEventQueue(pub)


@pytest.fixture()
def subscriber_1_calls():
    return []


@pytest.fixture()
def subscriber_2_calls():
    return []


@pytest.fixture
def subscriber_1(subscriber_1_calls):
    def fn(event, topic=pub.AUTO_TOPIC):
        subscriber_1_calls.append(topic.getName())

    return fn


@pytest.fixture
def subscriber_2(subscriber_2_calls):
    def fn(event, topic=pub.AUTO_TOPIC):
        subscriber_2_calls.append(topic.getName())

    return fn


@pytest.mark.usefixtures("subscriber_1", "subscriber_2", "subscriber_1_calls", "subscriber_2_calls")
def test_topic_subscription(subscriber_1, subscriber_2, subscriber_1_calls, subscriber_2_calls):
    pypubsub_event_queue.subscribe_type(TestEvent, subscriber_1)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_2, subscriber_1)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_1, subscriber_2)
    pypubsub_event_queue.publish(TestEvent(tags={EVENT_TAG_1, EVENT_TAG_2}))

    assert subscriber_1_calls == [TestEvent.__name__, EVENT_TAG_2]
    assert subscriber_2_calls == [EVENT_TAG_1]


def test_subscribe_all():
    subscriber_calls = []

    def subscriber(event, topic=pub.AUTO_TOPIC):
        subscriber_calls.append(topic.getName())

    pypubsub_event_queue.subscribe_all_events(subscriber)
    pypubsub_event_queue.publish(TestEvent(tags={EVENT_TAG_1, EVENT_TAG_2}))

    assert len(subscriber_calls) == 1
    assert TestEvent.__name__ not in subscriber_calls
    assert EVENT_TAG_1 not in subscriber_calls
    assert EVENT_TAG_2 not in subscriber_calls


@pytest.mark.usefixtures("subscriber_1", "subscriber_1_calls")
def test_subscribe_types(subscriber_1, subscriber_1_calls):
    pypubsub_event_queue.subscribe_type(TestEvent, subscriber_1)
    pypubsub_event_queue.publish(TestEvent(tags={EVENT_TAG_1, EVENT_TAG_2}))

    assert subscriber_1_calls == [TestEvent.__name__]


@pytest.mark.usefixtures("subscriber_1", "subscriber_2", "subscriber_1_calls", "subscriber_2_calls")
def test_subscribe_tags(subscriber_1, subscriber_2, subscriber_1_calls, subscriber_2_calls):
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_1, subscriber_1)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_2, subscriber_2)
    pypubsub_event_queue.publish(TestEvent(tags={EVENT_TAG_1, EVENT_TAG_2}))

    assert subscriber_1_calls == [EVENT_TAG_1]
    assert subscriber_2_calls == [EVENT_TAG_2]
