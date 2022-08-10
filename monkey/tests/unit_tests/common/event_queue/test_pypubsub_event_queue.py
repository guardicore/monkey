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
class TestEvent1(AbstractEvent):
    source: UUID = "f811ad00-5a68-4437-bd51-7b5cc1768ad5"
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet = frozenset()


@dataclass(frozen=True)
class TestEvent2(AbstractEvent):
    source: UUID = "e810ad01-6b67-9446-fc58-9b8d717653f7"
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet = frozenset()


def new_subscriber():
    def fn(event):
        fn.call_count += 1
        fn.call_types.add(event.__class__)
        fn.call_tags |= event.tags

    fn.call_count = 0
    fn.call_types = set()
    fn.call_tags = set()

    return fn


@pytest.fixture
def subscriber():
    return new_subscriber()


@pytest.fixture
def event_queue():
    return PyPubSubEventQueue(pub)


def test_subscribe_all(event_queue, subscriber):
    event_queue.subscribe_all_events(subscriber)

    event_queue.publish(TestEvent1(tags={EVENT_TAG_1, EVENT_TAG_2}))
    event_queue.publish(TestEvent1(tags={EVENT_TAG_2}))
    event_queue.publish(TestEvent1(tags={"secret_tag"}))
    event_queue.publish(TestEvent2())

    assert subscriber.call_count == 4
    assert TestEvent1 in subscriber.call_types
    assert TestEvent2 in subscriber.call_types


@pytest.mark.parametrize("type_to_subscribe", [TestEvent1, TestEvent2])
def test_subscribe_types(event_queue, subscriber, type_to_subscribe):
    event_queue.subscribe_type(type_to_subscribe, subscriber)

    event_queue.publish(TestEvent1())
    event_queue.publish(TestEvent2())

    assert subscriber.call_count == 1
    assert type_to_subscribe in subscriber.call_types


def test_subscribe_tags_single_type(event_queue, subscriber):
    event_queue.subscribe_tag(EVENT_TAG_1, subscriber)

    event_queue.publish(TestEvent1(tags={EVENT_TAG_1, EVENT_TAG_2}))
    event_queue.publish(TestEvent2(tags={EVENT_TAG_2}))

    assert subscriber.call_count == 1
    assert len(subscriber.call_types) == 1
    assert TestEvent1 in subscriber.call_types
    assert EVENT_TAG_1 in subscriber.call_tags


def test_subscribe_tags_multiple_types(event_queue, subscriber):
    event_queue.subscribe_tag(EVENT_TAG_2, subscriber)

    event_queue.publish(TestEvent1(tags={EVENT_TAG_1, EVENT_TAG_2}))
    event_queue.publish(TestEvent2(tags={EVENT_TAG_2}))

    assert subscriber.call_count == 2
    assert len(subscriber.call_types) == 2
    assert TestEvent1 in subscriber.call_types
    assert TestEvent2 in subscriber.call_types
    assert {EVENT_TAG_1, EVENT_TAG_2}.issubset(subscriber.call_tags)
