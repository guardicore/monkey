import pytest
import requests
import requests_mock

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


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client(actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI, exc=actual_error)

        with pytest.raises(expected_error):
            HTTPIslandAPIClient(SERVER)


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client__status_code(status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI, status_code=status_code)

        with pytest.raises(expected_error):
            HTTPIslandAPIClient(SERVER)


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client__send_log(actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client = HTTPIslandAPIClient(SERVER)

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
def test_island_api_client_send_log__status_code(status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client = HTTPIslandAPIClient(SERVER)

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
def test_island_api_client__get_pba_file(actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client = HTTPIslandAPIClient(SERVER)

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
def test_island_api_client_get_pba_file__status_code(status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client = HTTPIslandAPIClient(SERVER)

        with pytest.raises(expected_error):
            m.get(ISLAND_GET_PBA_FILE_URI, status_code=status_code)
            island_api_client.get_pba_file(filename=PBA_FILE)


@pytest.mark.parametrize(
    "actual_error, expected_error",
    [
        (requests.exceptions.ConnectionError, IslandAPIConnectionError),
        (TimeoutError, IslandAPITimeoutError),
        (Exception, IslandAPIError),
    ],
)
def test_island_api_client__send_events(actual_error, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client = HTTPIslandAPIClient(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_EVENTS_URI, exc=actual_error)
            island_api_client.send_events(events="some_data")


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (401, IslandAPIRequestError),
        (501, IslandAPIRequestFailedError),
    ],
)
def test_island_api_client_send_events__status_code(status_code, expected_error):
    with requests_mock.Mocker() as m:
        m.get(ISLAND_URI)
        island_api_client = HTTPIslandAPIClient(SERVER)

        with pytest.raises(expected_error):
            m.post(ISLAND_SEND_EVENTS_URI, status_code=status_code)
            island_api_client.send_events(events="some_data")
