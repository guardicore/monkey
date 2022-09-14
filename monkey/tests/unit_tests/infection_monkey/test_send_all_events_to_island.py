import time

import pytest
import requests_mock

from infection_monkey.send_all_events_to_island import AgentEventsToIslandSender
from monkey.infection_monkey.send_all_events_to_island import EVENTS_API_URL

SERVER = "1.1.1.1:9999"


@pytest.fixture
def event_sender():
    return AgentEventsToIslandSender(SERVER)


# @pytest.mark.skipif(os.name != "posix", reason="This test is racey on Windows")
def test_send_events(event_sender):
    with requests_mock.Mocker() as mock:
        mock.post(EVENTS_API_URL % SERVER)

        event_sender.start()

        for _ in range(5):
            event_sender.add_event_to_queue({})
        time.sleep(1)
        assert mock.call_count == 5

        event_sender.add_event_to_queue({})
        time.sleep(1)
        assert mock.call_count == 6

        event_sender.stop()
