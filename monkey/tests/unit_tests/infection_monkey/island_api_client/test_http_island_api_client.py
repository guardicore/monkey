import pytest
import requests
import requests_mock

from infection_monkey.island_api_client import (
    HTTPIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPITimeoutError,
)

SERVER = "1.1.1.1:9999"
PBA_FILE = "dummy.pba"

ISLAND_URI = f"https://{SERVER}/api?action=is-up"
ISLAND_SEND_LOG_URI = f"https://{SERVER}/api/log"
ISLAND_GET_PBA_FILE_URI = f"https://{SERVER}/api/pba/download/{PBA_FILE}"


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
