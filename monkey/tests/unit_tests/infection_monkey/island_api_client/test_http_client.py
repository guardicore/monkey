from unittest.mock import MagicMock
from uuid import UUID

import pytest
import requests
import requests_mock
from urllib3.exceptions import ConnectTimeoutError

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
AGENT_ID = UUID("80988359-a1cd-42a2-9b47-5b94b37cd673")

ISLAND_URI = f"https://{SERVER}/api?action=is-up"
LOG_ENDPOINT = f"/agent-logs/{AGENT_ID}"
ISLAND_SEND_LOG_URI = f"https://{SERVER}/api{LOG_ENDPOINT}"
PROPAGATION_CREDENTIALS_ENDPOINT = "/propagation-credentials"
ISLAND_GET_PROPAGATION_CREDENTIALS_URI = f"https://{SERVER}/api{PROPAGATION_CREDENTIALS_ENDPOINT}"


@pytest.fixture
def request_mock_instance():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def connected_client(request_mock_instance):
    http_client = HTTPClient()
    http_client.server_url = f"https://{SERVER}/api"
    request_mock_instance.get(ISLAND_URI)
    return http_client


@pytest.mark.parametrize(
    "initial_error, raised_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
    ],
)
def test_http_client__error_handling(
    initial_error, raised_error, connected_client, request_mock_instance
):
    request_mock_instance.get(ISLAND_GET_PROPAGATION_CREDENTIALS_URI, exc=initial_error)

    with pytest.raises(raised_error):
        connected_client.get(PROPAGATION_CREDENTIALS_ENDPOINT)


def test_http_client__unsupported_protocol():
    client = HTTPClient()

    with pytest.raises(RuntimeError):
        client.server_url = "http://1.1.1.1:5000"


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_http_client__status_handling(
    status_code, expected_error, connected_client, request_mock_instance
):
    request_mock_instance.put(ISLAND_SEND_LOG_URI, status_code=status_code)

    with pytest.raises(expected_error):
        connected_client.put(LOG_ENDPOINT, "Fake log contents")


def test_http_client__incorrect_call(connected_client, request_mock_instance):
    request_mock_instance.get(ISLAND_SEND_LOG_URI)

    # get requests have no data/json
    with pytest.raises(IslandAPIError):
        connected_client.get(LOG_ENDPOINT, hokus_pokus="something")


def test_http_client__unconnected():
    http_client = HTTPClient()

    with requests_mock.Mocker() as m:
        m.get(ISLAND_SEND_LOG_URI)

        with pytest.raises(IslandAPIError):
            http_client.get(LOG_ENDPOINT)


def test_http_client__retries(monkeypatch):
    http_client = HTTPClient()
    # skip the connect method
    http_client._server_url = f"https://{SERVER}/api"
    mock_send = MagicMock(side_effect=ConnectTimeoutError)
    # requests_mock can't be used for this, because it mocks higher level than we are testing
    monkeypatch.setattr("urllib3.connectionpool.HTTPSConnectionPool._validate_conn", mock_send)

    with pytest.raises(IslandAPIConnectionError):
        http_client.get(LOG_ENDPOINT)

    assert mock_send.call_count == RETRIES + 1


def test_http_client__additional_args(monkeypatch, connected_client):
    get = MagicMock()
    monkeypatch.setattr("requests.Session.get", get)

    connected_client.get(LOG_ENDPOINT, auth="authentication")

    assert get.call_args[1]["auth"] == "authentication"


def test_http_client__post(connected_client, monkeypatch):
    post = MagicMock()
    monkeypatch.setattr("requests.Session.post", post)

    connected_client.post(PROPAGATION_CREDENTIALS_ENDPOINT, data={"foo": "bar"}, timeout=10)

    assert post.call_args[1]["json"] == {"foo": "bar"}
    assert post.call_args[1]["timeout"] == 10


def test_http_client__put(connected_client, monkeypatch):
    put = MagicMock()
    monkeypatch.setattr("requests.Session.put", put)

    connected_client.put(PROPAGATION_CREDENTIALS_ENDPOINT, data={"foo": "bar"}, timeout=10)

    assert put.call_args[1]["json"] == {"foo": "bar"}
    assert put.call_args[1]["timeout"] == 10
