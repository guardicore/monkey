from typing import Any, Callable

import pytest
from pubsub import pub
from pubsub.core import Publisher

from common.event_queue import (
    IIslandEventQueue,
    IslandEventSubscriber,
    IslandEventTopic,
    PyPubSubIslandEventQueue,
)


@pytest.fixture
def event_queue() -> IIslandEventQueue:
    return PyPubSubIslandEventQueue(Publisher())


@pytest.fixture
def event_queue_subscriber() -> Callable[..., None]:
    def fn(event, topic=pub.AUTO_TOPIC):
        fn.call_count += 1
        fn.call_topics |= {topic.getName()}

    fn.call_count = 0
    fn.call_topics = set()

    return fn


def test_subscribe_publish(
    event_queue: IIslandEventQueue, event_queue_subscriber: IslandEventSubscriber
):
    event_queue.subscribe(topic=IslandEventTopic.AGENT_CONNECTED, subscriber=event_queue_subscriber)
    event_queue.subscribe(
        topic=IslandEventTopic.CLEAR_SIMULATION_DATA, subscriber=event_queue_subscriber
    )

    event_queue.publish(topic=IslandEventTopic.AGENT_CONNECTED)
    event_queue.publish(topic=IslandEventTopic.CLEAR_SIMULATION_DATA)
    event_queue.publish(topic=IslandEventTopic.RESET_AGENT_CONFIGURATION)

    assert event_queue_subscriber.call_count == 2
    assert event_queue_subscriber.call_topics == {
        IslandEventTopic.AGENT_CONNECTED.name,
        IslandEventTopic.CLEAR_SIMULATION_DATA.name,
    }


def test_keep_subscriber_in_scope(event_queue: IIslandEventQueue):
    class MyCallable:
        called = False

        def __call__(self, event: Any):
            MyCallable.called = True

    def subscribe():
        # fn will go out of scope after subscribe() returns.
        fn = MyCallable()
        event_queue.subscribe(topic=IslandEventTopic.AGENT_CONNECTED, subscriber=fn)

    subscribe()

    event_queue.publish(topic=IslandEventTopic.AGENT_CONNECTED)

    assert MyCallable.called
