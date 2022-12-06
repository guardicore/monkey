from ipaddress import IPv4Address
from multiprocessing import Queue
from time import sleep
from typing import FrozenSet, Union
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common.agent_events import AbstractAgentEvent
from common.event_queue import IAgentEventQueue
from infection_monkey.agent_event_handlers.plugin_event_forwarder import PluginEventForwarder


class FakeEvent(AbstractAgentEvent):
    source: UUID = UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5")
    target: Union[UUID, IPv4Address, None] = None
    timestamp: float = 0.0
    tags: FrozenSet = frozenset()


@pytest.fixture
def mock_agent_event_queue():
    return MagicMock(spec=IAgentEventQueue)


@pytest.fixture
def multiprocessing_queue():
    return Queue()


@pytest.fixture
def plugin_event_forwarder(multiprocessing_queue, mock_agent_event_queue):
    return PluginEventForwarder(multiprocessing_queue, mock_agent_event_queue, 0.01)


def test_no_events_in_queue(plugin_event_forwarder, mock_agent_event_queue):
    plugin_event_forwarder.start()
    plugin_event_forwarder.stop()

    assert mock_agent_event_queue.publish.call_count == 0


def test_multiple_events_in_queue_published(
    plugin_event_forwarder, multiprocessing_queue, mock_agent_event_queue
):
    for timestamp in range(5):
        multiprocessing_queue.put(FakeEvent(timestamp=timestamp))

    plugin_event_forwarder.start()
    # sleep(0.01)
    plugin_event_forwarder.stop()

    assert mock_agent_event_queue.publish.call_count == 5
