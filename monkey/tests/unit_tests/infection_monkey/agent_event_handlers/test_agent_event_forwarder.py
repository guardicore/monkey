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
    return BatchingAgentEventForwarder(mock_island_api_client)


def test_send_multiple_events_in_one_api_call(event_sender, mock_island_api_client):
    for _ in range(5):
        event_sender.add_event_to_queue({})

    event_sender.flush()

    assert mock_island_api_client.send_events.call_count == 1


def test_api_not_called_if_no_events(event_sender, mock_island_api_client):
    event_sender.flush()

    assert mock_island_api_client.send_events.call_count == 0


def test_resend_events_on_failure(event_sender, mock_island_api_client):
    mock_island_api_client.send_events = MagicMock(side_effect=Exception)
    events = [{"value": 1}, {"value": 2}, {"value": 3}]
    for e in events:
        event_sender.add_event_to_queue(e)

    event_sender.flush()
    event_sender.flush()

    assert mock_island_api_client.send_events.call_count == 2
    assert (
        mock_island_api_client.send_events.call_args_list[0]
        == mock_island_api_client.send_events.call_args_list[1]
    )
