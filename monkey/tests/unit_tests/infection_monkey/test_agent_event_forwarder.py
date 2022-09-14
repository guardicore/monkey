import time

import pytest
import requests_mock

from infection_monkey.agent_event_forwarder import EVENTS_API_URL, BatchingAgentEventForwarder

SERVER = "1.1.1.1:9999"


@pytest.fixture
def event_sender():
    return BatchingAgentEventForwarder(SERVER, time_period=0.001)


def test_send_events(event_sender):
    with requests_mock.Mocker() as mock:
        mock.post(EVENTS_API_URL % SERVER)

        event_sender.start()

        for _ in range(5):
            event_sender.add_event_to_queue({})
        time.sleep(0.01)
        assert mock.call_count == 1

        event_sender.add_event_to_queue({})
        time.sleep(0.01)
        assert mock.call_count == 2

        event_sender.stop()


def test_send_remaining_events(event_sender):
    with requests_mock.Mocker() as mock:
        mock.post(EVENTS_API_URL % SERVER)

        event_sender.start()

        for _ in range(5):
            event_sender.add_event_to_queue({})
        time.sleep(0.01)
        assert mock.call_count == 1

        event_sender.add_event_to_queue({})
        event_sender.stop()
        assert mock.call_count == 2
