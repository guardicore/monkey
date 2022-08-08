from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

import common.event_queue.pypubsub_event_queue as pypubsub_event_queue_file
from common.event_queue.pypubsub_event_queue import PypubsubEventQueue
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
    pypubsub_event_queue_file.pub.sendMessage = MagicMock(
        side_effect=pypubsub_event_queue_file.pub.sendMessage
    )


def test_subscribe_all():
    subscriber = MagicMock()

    PypubsubEventQueue.subscribe_all(subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 3


def test_subscribe_types():
    subscriber = MagicMock()

    PypubsubEventQueue.subscribe_types([EventType], subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 1


def test_subscribe_tags():
    subscriber = MagicMock()

    PypubsubEventQueue.subscribe_tags([EVENT_TAG_2], subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 1


def test_unsubscribe_all():
    subscriber = MagicMock()

    PypubsubEventQueue.subscribe_all(subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 3

    PypubsubEventQueue.unsubscribe_all(subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 6
    assert subscriber.call_count == 3


def test_unsubscribe_types():
    subscriber = MagicMock()

    PypubsubEventQueue.subscribe_all(subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 3

    PypubsubEventQueue.unsubscribe_types([EventType], subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 6
    assert subscriber.call_count == 5


def test_unsubscribe_tags():
    subscriber = MagicMock()

    PypubsubEventQueue.subscribe_all(subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 3

    PypubsubEventQueue.unsubscribe_tags([EVENT_TAG_1, EVENT_TAG_2], subscriber)
    PypubsubEventQueue.publish(EventType)

    assert pypubsub_event_queue_file.pub.sendMessage.call_count == 6
    assert subscriber.call_count == 4
