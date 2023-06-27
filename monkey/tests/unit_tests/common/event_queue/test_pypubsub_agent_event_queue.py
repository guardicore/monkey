from ipaddress import IPv4Address
from typing import Callable, FrozenSet, Union
from uuid import UUID

import pytest
from pubsub.core import Publisher

from common.agent_events import AbstractAgentEvent, AgentEventTag
from common.event_queue import AgentEventSubscriber, IAgentEventQueue, PyPubSubAgentEventQueue

EVENT_TAG_1 = "event-tag-1"
EVENT_TAG_2 = "event-tag-2"


class FakeEvent1(AbstractAgentEvent):
    source: UUID = UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5")
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet[AgentEventTag] = frozenset()


class FakeEvent2(AbstractAgentEvent):
    source: UUID = UUID("e810ad01-6b67-9446-fc58-9b8d717653f7")
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet[AgentEventTag] = frozenset()


@pytest.fixture
def event_queue() -> IAgentEventQueue:
    return PyPubSubAgentEventQueue(Publisher())


@pytest.fixture
def event_queue_subscriber() -> Callable[[AbstractAgentEvent], None]:
    def fn(event: AbstractAgentEvent):
        fn.call_count += 1
        fn.call_types.add(event.__class__)
        fn.call_tags |= event.tags

    fn.call_count = 0
    fn.call_types = set()
    fn.call_tags = set()

    return fn


def test_subscribe_all(event_queue: IAgentEventQueue, event_queue_subscriber: AgentEventSubscriber):
    event_queue.subscribe_all_events(event_queue_subscriber)

    event_queue.publish(FakeEvent1(tags=frozenset({EVENT_TAG_1, EVENT_TAG_2})))
    event_queue.publish(FakeEvent1(tags=frozenset({EVENT_TAG_2})))
    event_queue.publish(FakeEvent1(tags=frozenset({"secret_tag"})))
    event_queue.publish(FakeEvent2())

    assert event_queue_subscriber.call_count == 4
    assert FakeEvent1 in event_queue_subscriber.call_types
    assert FakeEvent2 in event_queue_subscriber.call_types


@pytest.mark.parametrize("type_to_subscribe", [FakeEvent1, FakeEvent2])
def test_subscribe_types(
    event_queue: IAgentEventQueue, event_queue_subscriber: AgentEventSubscriber, type_to_subscribe
):
    event_queue.subscribe_type(type_to_subscribe, event_queue_subscriber)

    event_queue.publish(FakeEvent1())
    event_queue.publish(FakeEvent2())

    assert event_queue_subscriber.call_count == 1
    assert type_to_subscribe in event_queue_subscriber.call_types


def test_subscribe_tags_single_type(
    event_queue: IAgentEventQueue, event_queue_subscriber: AgentEventSubscriber
):
    event_queue.subscribe_tag(EVENT_TAG_1, event_queue_subscriber)

    event_queue.publish(FakeEvent1(tags=frozenset({EVENT_TAG_1, EVENT_TAG_2})))
    event_queue.publish(FakeEvent2(tags=frozenset({EVENT_TAG_2})))

    assert event_queue_subscriber.call_count == 1
    assert len(event_queue_subscriber.call_types) == 1
    assert FakeEvent1 in event_queue_subscriber.call_types
    assert EVENT_TAG_1 in event_queue_subscriber.call_tags


def test_subscribe_tags_multiple_types(
    event_queue: IAgentEventQueue, event_queue_subscriber: AgentEventSubscriber
):
    event_queue.subscribe_tag(EVENT_TAG_2, event_queue_subscriber)

    event_queue.publish(FakeEvent1(tags=frozenset({EVENT_TAG_1, EVENT_TAG_2})))
    event_queue.publish(FakeEvent2(tags=frozenset({EVENT_TAG_2})))

    assert event_queue_subscriber.call_count == 2
    assert len(event_queue_subscriber.call_types) == 2
    assert FakeEvent1 in event_queue_subscriber.call_types
    assert FakeEvent2 in event_queue_subscriber.call_types
    assert {EVENT_TAG_1, EVENT_TAG_2}.issubset(event_queue_subscriber.call_tags)


def test_type_tag_collision(
    event_queue: IAgentEventQueue, event_queue_subscriber: AgentEventSubscriber
):
    event_queue.subscribe_type(FakeEvent1, event_queue_subscriber)

    event_queue.publish(FakeEvent2(tags=frozenset({FakeEvent1.__name__})))

    assert event_queue_subscriber.call_count == 0


def test_keep_subscriber_in_scope(event_queue: IAgentEventQueue):
    class MyCallable:
        called = False

        def __call__(self, event: AbstractAgentEvent):
            MyCallable.called = True

    def subscribe():
        # fn will go out of scope after subscribe() returns.
        fn = MyCallable()
        event_queue.subscribe_all_events(fn)

    subscribe()

    event_queue.publish(FakeEvent2())

    assert MyCallable.called
