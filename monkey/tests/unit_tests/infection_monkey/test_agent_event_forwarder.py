import time
from unittest.mock import MagicMock

import pytest

from infection_monkey.agent_event_handlers.agent_event_forwarder import BatchingAgentEventForwarder
from infection_monkey.island_api_client import IIslandAPIClient

SERVER = "1.1.1.1:9999"


@pytest.fixture
def mock_island_api_client():
    return MagicMock(spec=IIslandAPIClient)


@pytest.fixture
def event_sender(mock_island_api_client):
    return BatchingAgentEventForwarder(mock_island_api_client, time_period=0.001)


# NOTE: If these tests are too slow or end up being racey, we can redesign AgentEventForwarder to
#       handle threading and simply command BatchingAgentEventForwarder when to send events.
#       BatchingAgentEventForwarder would have unit tests, but AgentEventForwarder would not.


def test_send_events(event_sender, mock_island_api_client):
    event_sender.start()

    for _ in range(5):
        event_sender.add_event_to_queue({})
    time.sleep(0.05)
    assert mock_island_api_client.send_events.call_count == 1

    event_sender.add_event_to_queue({})
    time.sleep(0.05)
    assert mock_island_api_client.send_events.call_count == 2

    event_sender.stop()


def test_send_remaining_events(event_sender, mock_island_api_client):
    event_sender.start()

    for _ in range(5):
        event_sender.add_event_to_queue({})
    time.sleep(0.05)
    assert mock_island_api_client.send_events.call_count == 1

    event_sender.add_event_to_queue({})
    event_sender.stop()
    assert mock_island_api_client.send_events.call_count == 2
