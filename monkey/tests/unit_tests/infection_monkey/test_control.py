from unittest import mock
from unittest.mock import MagicMock

import pytest
import requests

from infection_monkey.network.relay import RELAY_CONTROL_MESSAGE
from monkey.common.network.network_utils import address_to_ip_port
from monkey.infection_monkey.control import ControlClient

SERVER_1 = "1.1.1.1:12312"
SERVER_2 = "2.2.2.2:4321"
SERVER_3 = "3.3.3.3:3142"
SERVER_4 = "4.4.4.4:5000"


class MockConnectionError:
    def __init__(self, *args, **kwargs):
        raise requests.exceptions.ConnectionError


class RequestsGetArgument:
    def __init__(self, *args, **kwargs):
        if SERVER_1 in args[0]:
            MockConnectionError()


@pytest.fixture
def servers():
    return [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


@pytest.mark.parametrize(
    "is_windows_os,expected_proxy_string",
    [(True, "http://8.8.8.8:45455"), (False, "8.8.8.8:45455")],
)
def test_control_set_proxies(monkeypatch, is_windows_os, expected_proxy_string):
    monkeypatch.setattr("monkey.infection_monkey.control.is_windows_os", lambda: is_windows_os)
    control_client = ControlClient("8.8.8.8:5000")

    control_client.set_proxies(("8.8.8.8", "45455"))

    assert control_client.proxies["https"] == expected_proxy_string


def test_control_find_server__no_available_relays(monkeypatch, servers):
    monkeypatch.setattr("infection_monkey.control.requests.get", MockConnectionError)

    cc = ControlClient(servers)

    assert cc.find_server(servers) is False
    assert servers == []


def test_control_find_server__control_message_sent_to_necessary_relays(monkeypatch, servers):
    mock_connect = MagicMock()
    mock_send = MagicMock()
    monkeypatch.setattr("infection_monkey.control.requests.get", RequestsGetArgument)
    monkeypatch.setattr("infection_monkey.control.socket.socket.connect", mock_connect)
    monkeypatch.setattr("infection_monkey.control.socket.socket.send", mock_send)

    cc = ControlClient(servers)

    return_value = cc.find_server(servers)

    assert len(servers) == 2
    assert return_value is True
    assert mock_connect.call_count == 2

    server_3_ip, server_3_port = address_to_ip_port(SERVER_3)
    server_4_ip, server_4_port = address_to_ip_port(SERVER_4)
    mock_connect.assert_has_calls(
        [mock.call((server_3_ip, int(server_3_port))), mock.call((server_4_ip, int(server_4_port)))]
    )

    assert mock_send.call_count == 2
    mock_send.assert_called_with(RELAY_CONTROL_MESSAGE)
