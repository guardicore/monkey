import json
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common import OperatingSystem
from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from infection_monkey.island_api_client import HTTPIslandAPIClient, IslandAPIRequestError
from infection_monkey.island_api_client.island_api_client_errors import (
    IslandAPIResponseParsingError,
)

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
ISLAND_SEND_HEARTBEAT_URI = f"https://{SERVER}/api/agent/{AGENT_ID}/heartbeat"


class Event1(AbstractAgentEvent):
    a: int


class Event2(AbstractAgentEvent):
    b: str


class Event3(AbstractAgentEvent):
    c: int


def agent_event_serializer_registry():
    agent_event_serializer_registry = AgentEventSerializerRegistry()
    agent_event_serializer_registry[Event1] = PydanticAgentEventSerializer(Event1)
    agent_event_serializer_registry[Event2] = PydanticAgentEventSerializer(Event2)

    return agent_event_serializer_registry


def build_api_client(http_client):
    return HTTPIslandAPIClient(agent_event_serializer_registry(), http_client)


def test_island_api_client__get_agent_binary():
    fake_binary = b"agent-binary"
    os = OperatingSystem.LINUX
    http_client_stub = MagicMock()
    response_stub = MagicMock()
    response_stub.content = fake_binary
    http_client_stub.get.return_value = response_stub
    api_client = build_api_client(http_client_stub)

    assert api_client.get_agent_binary(os) == fake_binary
    assert http_client_stub.get.called_with("agent-binaries/linux")


def test_island_api_client_send_events__serialization():
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
    client_spy = MagicMock()
    api_client = build_api_client(client_spy)

    api_client.send_events(events=events_to_send)

    assert client_spy.post.call_args[0] == ("agent-events", expected_json)


def test_island_api_client_send_events__serialization_failed():
    client_spy = MagicMock()
    api_client = build_api_client(client_spy)

    with pytest.raises(IslandAPIRequestError):
        api_client.send_events(events=[Event3(source=AGENT_ID, c=1)])


def test_island_api_client__unhandled_exceptions():
    # Make sure errors not related to response parsing are not handled
    http_client_stub = MagicMock()
    http_client_stub.get = MagicMock(side_effect=OSError)
    api_client = build_api_client(http_client_stub)

    with pytest.raises(OSError):
        api_client.get_agent_signals(agent_id=AGENT_ID)


def test_island_api_client__handled_exceptions():
    http_client_stub = MagicMock()
    http_client_stub.get = MagicMock(side_effect=json.JSONDecodeError)
    api_client = build_api_client(http_client_stub)

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_agent_signals(agent_id=AGENT_ID)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_send_heartbeat__status_code(
    island_api_client, status_code, expected_error
):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_HEARTBEAT_URI, status_code=status_code)
            island_api_client.send_heartbeat(agent_id=AGENT_ID, timestamp=TIMESTAMP)


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client_send_heartbeat__errors(island_api_client, actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client.connect(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_HEARTBEAT_URI, exc=actual_error)
            island_api_client.send_heartbeat(agent_id=AGENT_ID, timestamp=TIMESTAMP)
