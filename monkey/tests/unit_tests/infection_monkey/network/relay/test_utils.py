import pytest
import requests

from infection_monkey.network.relay.utils import find_server

SERVER_1 = "1.1.1.1:12312"
SERVER_2 = "2.2.2.2:4321"
SERVER_3 = "3.3.3.3:3142"
SERVER_4 = "4.4.4.4:5000"


class MockConnectionError:
    def __init__(self, *args, **kwargs):
        raise requests.exceptions.ConnectionError


class MockRequestsGetResponsePerServerArgument:
    def __init__(self, *args, **kwargs):
        if SERVER_1 in args[0]:
            MockConnectionError()


@pytest.fixture
def servers():
    return [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


@pytest.mark.parametrize(
    "mock_requests_get, expected",
    [(MockConnectionError, None), (MockRequestsGetResponsePerServerArgument, SERVER_2)],
)
def test_find_server__no_available_relays(monkeypatch, servers, mock_requests_get, expected):
    monkeypatch.setattr("infection_monkey.control.requests.get", mock_requests_get)

    assert find_server(servers) is expected
