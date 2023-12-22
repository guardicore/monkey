from ipaddress import IPv4Address
from multiprocessing import Queue
from typing import FrozenSet, Union
from uuid import UUID

import pytest
from monkeyevents import AbstractAgentEvent

from common.event_queue import QueuedAgentEventPublisher


class FakeEvent(AbstractAgentEvent):
    source: UUID = UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5")
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet = frozenset()


@pytest.fixture
def multiprocessing_queue() -> Queue:
    return Queue()


@pytest.fixture
def queued_agent_event_publisher(multiprocessing_queue):
    return QueuedAgentEventPublisher(multiprocessing_queue)


def test_queue_agent_event_publisher(queued_agent_event_publisher, multiprocessing_queue):
    expected_event = FakeEvent()
    queued_agent_event_publisher.publish(expected_event)

    actual_event = multiprocessing_queue.get(timeout=0.001)

    assert actual_event == expected_event
