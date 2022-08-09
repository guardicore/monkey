from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest
from pubsub import pub

from common.event_queue.pypubsub_event_queue import PyPubSubEventQueue
from common.events import AbstractEvent

EVENT_TAG_1 = "event tag 1"
EVENT_TAG_2 = "event tag 2"


@dataclass(frozen=True)
class EventType(AbstractEvent):
    source = "1234"
    target = None
    timestamp = 0.0
    tags = [EVENT_TAG_1, EVENT_TAG_2]


@pytest.fixture(autouse=True)
def wrap_pypubsub_functions():
    # This is done so that we can use `.call_count` in the tests.
    pub.sendMessage = MagicMock(side_effect=pub.sendMessage)


pypubsub_event_queue = PyPubSubEventQueue(pub)


def test_subscribe_all():
    subscriber = MagicMock()

    pypubsub_event_queue.subscribe_all(subscriber)
    pypubsub_event_queue.publish(EventType)

    assert pub.sendMessage.call_count == 3
    assert subscriber.call_count == 3


def test_subscribe_types():
    subscriber = MagicMock()

    pypubsub_event_queue.subscribe_type(EventType, subscriber)
    pypubsub_event_queue.publish(EventType)

    assert pub.sendMessage.call_count == 3
    assert subscriber.call_count == 1


def test_subscribe_tags():
    subscriber = MagicMock()

    pypubsub_event_queue.subscribe_tag(EVENT_TAG_1, subscriber)
    pypubsub_event_queue.subscribe_tag(EVENT_TAG_2, subscriber)
    pypubsub_event_queue.publish(EventType)

    assert pub.sendMessage.call_count == 3
    assert subscriber.call_count == 2
