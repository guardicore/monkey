from uuid import UUID

import pytest
import requests
import requests_mock

from common import AgentSignals, OperatingSystem
from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from common.agent_registration_data import AgentRegistrationData
from common.types import SocketAddress
from infection_monkey.island_api_client import (
    HTTPIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)

SERVER = SocketAddress(ip="1.1.1.1", port=9999)
WINDOWS = "windows"
AGENT_ID = UUID("80988359-a1cd-42a2-9b47-5b94b37cd673")
AGENT_REGISTRATION = AgentRegistrationData(
    id=AGENT_ID,
    machine_hardware_id=1,
    start_time=0,
    parent_id=None,
    cc_server=SERVER,
    network_interfaces=[],
)

TIMESTAMP = 123456789

ISLAND_URI = f"https://{SERVER}/api?action=is-up"
ISLAND_SEND_LOG_URI = f"https://{SERVER}/api/agent-logs/{AGENT_ID}"
ISLAND_GET_AGENT_BINARY_URI = f"https://{SERVER}/api/agent-binaries/{WINDOWS}"
ISLAND_SEND_EVENTS_URI = f"https://{SERVER}/api/agent-events"
ISLAND_REGISTER_AGENT_URI = f"https://{SERVER}/api/agents"
ISLAND_AGENT_STOP_URI = f"https://{SERVER}/api/monkey-control/needs-to-stop/{AGENT_ID}"
ISLAND_GET_CONFIG_URI = f"https://{SERVER}/api/agent-configuration"
ISLAND_GET_PROPAGATION_CREDENTIALS_URI = f"https://{SERVER}/api/propagation-credentials"
ISLAND_GET_AGENT_SIGNALS = f"https://{SERVER}/api/agent-signals/{AGENT_ID}"


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
            m.put(ISLAND_SEND_LOG_URI, exc=actual_error)
            island_api_client.send_log(agent_id=AGENT_ID, log_contents="some_data")


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
            m.put(ISLAND_SEND_LOG_URI, status_code=status_code)
            island_api_client.send_log(agent_id=AGENT_ID, log_contents="some_data")


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client__get_agent_binary(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_AGENT_BINARY_URI, exc=actual_error)
            island_api_client.get_agent_binary(operating_system=OperatingSystem.WINDOWS)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client__get_agent_binary_status_code(
    island_api_client, status_code, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_AGENT_BINARY_URI, status_code=status_code)
            island_api_client.get_agent_binary(operating_system=OperatingSystem.WINDOWS)


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


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
    ],
)
def test_island_api_client__register_agent(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_REGISTER_AGENT_URI, exc=actual_error)
            island_api_client.register_agent(AGENT_REGISTRATION)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_register_agent__status_code(
    island_api_client, status_code, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_REGISTER_AGENT_URI, status_code=status_code)
            island_api_client.register_agent(AGENT_REGISTRATION)


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
    ],
)
def test_island_api_client__get_config(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_CONFIG_URI, exc=actual_error)
            island_api_client.get_config()


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_get_config__status_code(island_api_client, status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_CONFIG_URI, status_code=status_code)
            island_api_client.get_config()


def test_island_api_client_get_config__bad_json(island_api_client):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(IslandAPIRequestFailedError):
            m.get(ISLAND_GET_CONFIG_URI, content=b"bad")
            island_api_client.get_config()


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
    ],
)
def test_island_api_client__get_credentials_for_propagation(
    island_api_client, actual_error, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_PROPAGATION_CREDENTIALS_URI, exc=actual_error)
            island_api_client.get_credentials_for_propagation()


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_get_credentials_for_propagation__status_code(
    island_api_client, status_code, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_PROPAGATION_CREDENTIALS_URI, status_code=status_code)
            island_api_client.get_credentials_for_propagation()


def test_island_api_client_get_credentials_for_propagation__bad_json(island_api_client):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(IslandAPIRequestFailedError):
            m.get(ISLAND_GET_PROPAGATION_CREDENTIALS_URI, content=b"bad")
            island_api_client.get_credentials_for_propagation()


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
    ],
)
def test_island_api_client__get_agent_signals(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_AGENT_SIGNALS, exc=actual_error)
            island_api_client.get_agent_signals(agent_id=AGENT_ID)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_get_agent_signals__status_code(
    island_api_client, status_code, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_AGENT_SIGNALS, status_code=status_code)
            island_api_client.get_agent_signals(agent_id=AGENT_ID)


@pytest.mark.parametrize("timestamp", [TIMESTAMP, None])
def test_island_api_client_get_agent_signals(island_api_client, timestamp):
    expected_agent_signals = AgentSignals(terminate=timestamp)
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        m.get(ISLAND_GET_AGENT_SIGNALS, json={"terminate": timestamp})
        actual_agent_signals = island_api_client.get_agent_signals(agent_id=AGENT_ID)

        assert actual_agent_signals == expected_agent_signals


def test_island_api_client_get_agent_signals__bad_json(island_api_client):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(IslandAPIError):
            m.get(ISLAND_GET_AGENT_SIGNALS, json={"bogus": "vogus"})
            island_api_client.get_agent_signals(agent_id=AGENT_ID)
