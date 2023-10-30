from unittest.mock import MagicMock
from uuid import UUID

import pytest
import requests
import requests_mock
from monkeytypes import SocketAddress
from urllib3.exceptions import ConnectTimeoutError

from infection_monkey.island_api_client import (
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPIRequestLimitExceededError,
    IslandAPITimeoutError,
)
from infection_monkey.island_api_client.http_client import RETRIES, HTTPClient
from infection_monkey.island_api_client.island_api_client_errors import IslandAPIAuthenticationError

SERVER = SocketAddress(ip="127.0.0.1", port=9999)
SERVER_URL = f"https://{SERVER}/api"
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
def http_client(request_mock_instance):
    http_client = HTTPClient(SERVER_URL)
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
    initial_error, raised_error, http_client, request_mock_instance
):
    request_mock_instance.get(ISLAND_GET_PROPAGATION_CREDENTIALS_URI, exc=initial_error)

    with pytest.raises(raised_error):
        http_client.get(PROPAGATION_CREDENTIALS_ENDPOINT)


@pytest.mark.parametrize("server", [f"http://{SERVER}", ""])
def test_http_client__unsupported_protocol(server):
    with pytest.raises(ValueError):
        HTTPClient(server)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIAuthenticationError),
        (403, IslandAPIAuthenticationError),
        (400, IslandAPIRequestError),
        (429, IslandAPIRequestLimitExceededError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_http_client__status_handling(
    status_code, expected_error, http_client, request_mock_instance
):
    request_mock_instance.put(ISLAND_SEND_LOG_URI, status_code=status_code)

    with pytest.raises(expected_error):
        http_client.put(LOG_ENDPOINT, "Fake log contents")


def test_http_client__incorrect_call(http_client, request_mock_instance):
    request_mock_instance.get(ISLAND_SEND_LOG_URI)

    # get requests have no data/json
    with pytest.raises(IslandAPIError):
        http_client.get(LOG_ENDPOINT, hokus_pokus="something")


def test_http_client__retries(monkeypatch):
    http_client = HTTPClient(SERVER_URL)
    mock_send = MagicMock(side_effect=ConnectTimeoutError)
    # requests_mock can't be used for this, because it mocks higher level than we are testing
    monkeypatch.setattr("urllib3.connectionpool.HTTPSConnectionPool._validate_conn", mock_send)

    with pytest.raises(IslandAPIConnectionError):
        http_client.get(LOG_ENDPOINT)

    assert mock_send.call_count == RETRIES + 1


def test_http_client__additional_args(monkeypatch, http_client):
    get = MagicMock()
    monkeypatch.setattr("requests.Session.get", get)

    http_client.get(LOG_ENDPOINT, auth="authentication")

    assert get.call_args[1]["auth"] == "authentication"


def test_http_client__post(http_client, monkeypatch):
    post = MagicMock()
    monkeypatch.setattr("requests.Session.post", post)

    http_client.post(PROPAGATION_CREDENTIALS_ENDPOINT, data={"foo": "bar"}, timeout=10)

    assert post.call_args[1]["json"] == {"foo": "bar"}
    assert post.call_args[1]["timeout"] == 10


def test_http_client__put(http_client, monkeypatch):
    put = MagicMock()
    monkeypatch.setattr("requests.Session.put", put)

    http_client.put(PROPAGATION_CREDENTIALS_ENDPOINT, data={"foo": "bar"}, timeout=10)

    assert put.call_args[1]["json"] == {"foo": "bar"}
    assert put.call_args[1]["timeout"] == 10
