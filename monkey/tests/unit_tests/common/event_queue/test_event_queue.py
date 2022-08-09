from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

import common.event_queue.event_queue as event_queue_file
from common.event_queue.event_queue import EventQueue
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
    event_queue_file.pub.sendMessage = MagicMock(side_effect=event_queue_file.pub.sendMessage)


def test_subscribe_all():
    subscriber = MagicMock()

    EventQueue.subscribe_all(subscriber)
    EventQueue.publish(EventType)

    assert event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 3


def test_subscribe_types():
    subscriber = MagicMock()

    EventQueue.subscribe_types([EventType], subscriber)
    EventQueue.publish(EventType)

    assert event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 1


def test_subscribe_tags():
    subscriber = MagicMock()

    EventQueue.subscribe_tags([EVENT_TAG_2], subscriber)
    EventQueue.publish(EventType)

    assert event_queue_file.pub.sendMessage.call_count == 3
    assert subscriber.call_count == 1
