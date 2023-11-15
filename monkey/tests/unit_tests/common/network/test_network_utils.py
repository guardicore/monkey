from ipaddress import IPv4Address
from unittest.mock import MagicMock, Mock

from psutil._common import addr

from common.network.network_utils import get_connections


def build_connection(ip, port):
    return Mock(laddr=addr(ip=ip, port=port))


def test_get_connections__connection_found(monkeypatch):
    connections = [
        build_connection("127.1.1.1", 443),
        build_connection("127.2.2.2", 443),
    ]
    monkeypatch.setattr("psutil.net_connections", MagicMock(return_value=connections))
    expected_connection = build_connection("127.2.2.2", 443)

    found_connections = get_connections(ports=[443], ip_addresses=[IPv4Address("127.2.2.2")])

    assert len(found_connections) == 1
    assert found_connections[0].laddr == expected_connection.laddr


def test_get_connections__no_connection_found(monkeypatch):
    connections = [
        build_connection("127.1.1.1", 443),
        build_connection("127.2.2.2", 443),
        build_connection("127.3.3.3", 123),
    ]
    monkeypatch.setattr("psutil.net_connections", MagicMock(return_value=connections))

    found_connections = get_connections(ip_addresses=[IPv4Address("127.3.3.3")], ports=[443])

    assert len(found_connections) == 0


def test_get_connections__all_connections(monkeypatch):
    connections = [
        build_connection("127.1.1.1", 443),
        build_connection("127.2.2.2", 443),
        build_connection("127.3.3.3", 123),
    ]
    monkeypatch.setattr("psutil.net_connections", MagicMock(return_value=connections))

    found_connections = get_connections()

    assert len(found_connections) == 3
    assert found_connections[0].laddr == connections[0].laddr
    assert found_connections[1].laddr == connections[1].laddr
    assert found_connections[2].laddr == connections[2].laddr
