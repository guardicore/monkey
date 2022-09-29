from unittest.mock import MagicMock

import pytest

from common.types import PortStatus
from infection_monkey.network_scanning import scan_tcp_ports
from infection_monkey.network_scanning.tcp_scanner import EMPTY_PORT_SCAN

PORTS_TO_SCAN = [22, 80, 8080, 143, 445, 2222]

OPEN_PORTS_DATA = {22: "SSH-banner", 80: "", 2222: "SSH2-banner"}


@pytest.fixture
def patch_check_tcp_ports(monkeypatch, open_ports_data):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.tcp_scanner._check_tcp_ports",
        lambda *_: open_ports_data,
    )


@pytest.mark.parametrize("open_ports_data", [OPEN_PORTS_DATA])
def test_tcp_successful(monkeypatch, patch_check_tcp_ports, open_ports_data):
    closed_ports = [8080, 143, 445]

    port_scan_data = scan_tcp_ports("127.0.0.1", PORTS_TO_SCAN, 0)

    assert len(port_scan_data) == 6
    for port in open_ports_data.keys():
        assert port_scan_data[port].port == port
        assert port_scan_data[port].status == PortStatus.OPEN
        assert port_scan_data[port].banner == open_ports_data.get(port)

    for port in closed_ports:
        assert port_scan_data[port].port == port
        assert port_scan_data[port].status == PortStatus.CLOSED
        assert port_scan_data[port].banner is None


@pytest.mark.parametrize("open_ports_data", [{}])
def test_tcp_empty_response(monkeypatch, patch_check_tcp_ports, open_ports_data):
    port_scan_data = scan_tcp_ports("127.0.0.1", PORTS_TO_SCAN, 0)

    assert len(port_scan_data) == 6
    for port in open_ports_data:
        assert port_scan_data[port].port == port
        assert port_scan_data[port].status == PortStatus.CLOSED
        assert port_scan_data[port].banner is None


@pytest.mark.parametrize("open_ports_data", [OPEN_PORTS_DATA])
def test_tcp_no_ports_to_scan(monkeypatch, patch_check_tcp_ports, open_ports_data):
    port_scan_data = scan_tcp_ports("127.0.0.1", [], 0)

    assert len(port_scan_data) == 0


def test_exception_handling(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.tcp_scanner._scan_tcp_ports",
        MagicMock(side_effect=Exception),
    )
    assert scan_tcp_ports("abc", [123], 123) == EMPTY_PORT_SCAN
