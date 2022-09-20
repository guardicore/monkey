from uuid import UUID

import pytest
import requests
import requests_mock

from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from infection_monkey.island_api_client import (
    HTTPIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)

SERVER = "1.1.1.1:9999"
PBA_FILE = "dummy.pba"

ISLAND_URI = f"https://{SERVER}/api?action=is-up"
ISLAND_SEND_LOG_URI = f"https://{SERVER}/api/log"
ISLAND_GET_PBA_FILE_URI = f"https://{SERVER}/api/pba/download/{PBA_FILE}"
ISLAND_SEND_EVENTS_URI = f"https://{SERVER}/api/agent-events"

AGENT_ID = UUID("80988359-a1cd-42a2-9b47-5b94b37cd673")


class Event1(AbstractAgentEvent):
    a: int


class Event2(AbstractAgentEvent):
    b: str


class Event3(AbstractAgentEvent):
    c: int


@pytest.fixture
def agent_event_serializer_registry():
    agent_event_serializer_registry = AgentEventSerializerRegistry()
    agent_event_serializer_registry[Event1] = PydanticAgentEventSerializer(Event1)
    agent_event_serializer_registry[Event2] = PydanticAgentEventSerializer(Event2)

    return agent_event_serializer_registry


@pytest.fixture
def island_api_client(agent_event_serializer_registry):
    return HTTPIslandAPIClient(agent_event_serializer_registry)


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI, exc=actual_error)

        with pytest.raises(expected_error):
            island_api_client.connect(SERVER)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client__status_code(island_api_client, status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI, status_code=status_code)

        with pytest.raises(expected_error):
            island_api_client.connect(SERVER)


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client__send_log(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_LOG_URI, exc=actual_error)
            island_api_client.send_log(log_contents="some_data")


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_send_log__status_code(island_api_client, status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_LOG_URI, status_code=status_code)
            island_api_client.send_log(log_contents="some_data")


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client__get_pba_file(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_PBA_FILE_URI, exc=actual_error)
            island_api_client.get_pba_file(filename=PBA_FILE)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_get_pba_file__status_code(
    island_api_client, status_code, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_PBA_FILE_URI, status_code=status_code)
            island_api_client.get_pba_file(filename=PBA_FILE)


def test_island_api_client_send_events__serialization(island_api_client):
    events_to_send = [
        Event1(source=AGENT_ID, timestamp=0, a=1),
        Event2(source=AGENT_ID, timestamp=0, b="hello"),
    ]
    expected_json = [
        {
            "source": "80988359-a1cd-42a2-9b47-5b94b37cd673",
            "target": None,
            "timestamp": 0.0,
            "tags": [],
            "a": 1,
            "type": "Event1",
        },
        {
            "source": "80988359-a1cd-42a2-9b47-5b94b37cd673",
            "target": None,
            "timestamp": 0.0,
            "tags": [],
            "b": "hello",
            "type": "Event2",
        },
    ]

    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        m.post(ISLAND_SEND_EVENTS_URI)
        island_api_client.connect(SERVER)

        island_api_client.send_events(events=events_to_send)

        assert m.last_request.json() == expected_json


def test_island_api_client_send_events__serialization_failed(island_api_client):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(IslandAPIRequestError):
            m.post(ISLAND_SEND_EVENTS_URI)
            island_api_client.send_events(events=[Event3(source=AGENT_ID, c=1)])


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client__send_events(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_EVENTS_URI, exc=actual_error)
            island_api_client.send_events(events=[Event1(source=AGENT_ID, a=1)])


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_send_events__status_code(island_api_client, status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_EVENTS_URI, status_code=status_code)
            island_api_client.send_events(events=[Event1(source=AGENT_ID, a=1)])
