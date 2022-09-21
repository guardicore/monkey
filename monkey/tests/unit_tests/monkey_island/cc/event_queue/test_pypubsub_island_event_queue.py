from typing import Callable

import pytest
from pubsub import pub
from pubsub.core import Publisher

from monkey_island.cc.event_queue import (
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
    class SubscriberSpy:
        call_count = 0
        call_topics = set()

        def __call__(self, topic=pub.AUTO_TOPIC):
            self.call_count += 1
            self.call_topics |= {topic.getName()}

    return SubscriberSpy()


def test_subscribe_publish__no_event_body(
    event_queue: IIslandEventQueue, event_queue_subscriber: IslandEventSubscriber
):
    event_queue.subscribe(
        topic=IslandEventTopic.RESET_AGENT_CONFIGURATION, subscriber=event_queue_subscriber
    )
    event_queue.subscribe(
        topic=IslandEventTopic.CLEAR_SIMULATION_DATA, subscriber=event_queue_subscriber
    )

    event_queue.publish(topic=IslandEventTopic.AGENT_REGISTERED)
    event_queue.publish(topic=IslandEventTopic.CLEAR_SIMULATION_DATA)
    event_queue.publish(topic=IslandEventTopic.RESET_AGENT_CONFIGURATION)

    assert event_queue_subscriber.call_count == 2
    assert event_queue_subscriber.call_topics == {
        IslandEventTopic.RESET_AGENT_CONFIGURATION.name,
        IslandEventTopic.CLEAR_SIMULATION_DATA.name,
    }


def test_subscribe_publish__with_event_body(
    event_queue: IIslandEventQueue, event_queue_subscriber: IslandEventSubscriber
):
    class MyCallable:
        call_count = 0
        event = None

        def __call__(self, event):
            self.call_count += 1
            self.event = event

    event = "my event!"
    my_callable = MyCallable()
    event_queue.subscribe(topic=IslandEventTopic.AGENT_REGISTERED, subscriber=my_callable)

    event_queue.publish(topic=IslandEventTopic.AGENT_REGISTERED, event=event)
    event_queue.publish(topic=IslandEventTopic.CLEAR_SIMULATION_DATA)
    event_queue.publish(topic=IslandEventTopic.RESET_AGENT_CONFIGURATION)

    assert my_callable.call_count == 1
    assert my_callable.event == event


def test_keep_subscriber_in_scope(event_queue: IIslandEventQueue):
    class MyCallable:
        called = False

        def __call__(self):
            MyCallable.called = True

    def subscribe():
        # fn will go out of scope after subscribe() returns.
        fn = MyCallable()
        event_queue.subscribe(topic=IslandEventTopic.AGENT_REGISTERED, subscriber=fn)

    subscribe()

    event_queue.publish(topic=IslandEventTopic.AGENT_REGISTERED)

    assert MyCallable.called
