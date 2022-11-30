from unittest.mock import MagicMock
from uuid import UUID

import pytest
import requests
import requests_mock
from urllib3.exceptions import ConnectTimeoutError

from common import AgentRegistrationData
from common.types import SocketAddress
from infection_monkey.island_api_client import (
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)
from infection_monkey.island_api_client.http_client import RETRIES, HTTPClient

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
LOG_ENDPOINT = f"agent-logs/{AGENT_ID}"
ISLAND_SEND_LOG_URI = f"https://{SERVER}/api/{LOG_ENDPOINT}"
ISLAND_GET_AGENT_BINARY_URI = f"https://{SERVER}/api/agent-binaries/{WINDOWS}"
ISLAND_SEND_EVENTS_URI = f"https://{SERVER}/api/agent-events"
ISLAND_REGISTER_AGENT_URI = f"https://{SERVER}/api/agents"
ISLAND_AGENT_STOP_URI = f"https://{SERVER}/api/monkey-control/needs-to-stop/{AGENT_ID}"
ISLAND_GET_CONFIG_URI = f"https://{SERVER}/api/agent-configuration"
PROPAGATION_CREDENTIALS_ENDPOINT = "propagation-credentials"
ISLAND_GET_PROPAGATION_CREDENTIALS_URI = f"https://{SERVER}/api/{PROPAGATION_CREDENTIALS_ENDPOINT}"
ISLAND_GET_AGENT_SIGNALS = f"https://{SERVER}/api/agent-signals/{AGENT_ID}"


@pytest.fixture
def connected_client():
    http_client = HTTPClient()

    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        http_client.connect(SERVER)
        yield {"client": http_client, "mock": m}


@pytest.mark.parametrize(
    "initial_error, raised_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
    ],
)
def test_http_client__error_handling(initial_error, raised_error, connected_client):
    with pytest.raises(raised_error):
        connected_client["mock"].get(ISLAND_GET_PROPAGATION_CREDENTIALS_URI, exc=initial_error)
        connected_client["client"].get(PROPAGATION_CREDENTIALS_ENDPOINT)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_http_client__status_handling(status_code, expected_error, connected_client):
    with pytest.raises(expected_error):
        connected_client["mock"].put(ISLAND_SEND_LOG_URI, status_code=status_code)
        connected_client["client"].put(LOG_ENDPOINT, "Fake log contents")


def test_http_client__incorrect_call(connected_client):
    with pytest.raises(IslandAPIError):
        connected_client["mock"].get(ISLAND_SEND_LOG_URI)
        # get requests have no data/json
        connected_client["client"].get(LOG_ENDPOINT, hokus_pokus="something")


def test_http_client__unconnected():
    http_client = HTTPClient()

    with requests_mock.Mocker() as m:
        with pytest.raises(IslandAPIError):
            m.get(ISLAND_SEND_LOG_URI)
            http_client.get(LOG_ENDPOINT)


def test_http_client_retries(monkeypatch):
    http_client = HTTPClient()

    # skip the connect method
    http_client._api_url = f"https://{SERVER}/api"

    # requests_mock can't be used for this, because it mocks higher level than we are testing
    with pytest.raises(IslandAPIConnectionError):
        mock_send = MagicMock(side_effect=ConnectTimeoutError)
        monkeypatch.setattr("urllib3.connectionpool.HTTPSConnectionPool._validate_conn", mock_send)
        http_client.get(LOG_ENDPOINT)

    assert mock_send.call_count == RETRIES + 1


def test_http_client__additional_args(monkeypatch, connected_client):
    get = MagicMock()
    monkeypatch.setattr("requests.Session.get", get)

    connected_client["client"].get(LOG_ENDPOINT, auth="authentication")
    assert get.call_args[1]["auth"] == "authentication"
