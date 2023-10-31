from unittest.mock import MagicMock

import pytest
from monkeytypes import AgentID, PortStatus

from common.agent_events import TCPScanEvent
from infection_monkey.i_puppet import PortScanData
from infection_monkey.network_scanning import scan_tcp_ports
from infection_monkey.network_scanning.tcp_scanner import EMPTY_PORT_SCAN

PORTS_TO_SCAN = [22, 80, 8080, 143, 445, 2222]

OPEN_PORTS_DATA = {22: "SSH-banner", 80: "", 2222: "SSH2-banner"}

TIMESTAMP = 123.321

HOST_IP = "127.0.0.1"
AGENT_ID = AgentID("b63e5ca3-e33b-4c3b-96d3-2e6f10d6e2d9")


@pytest.fixture(autouse=True)
def patch_timestamp(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.tcp_scanner.time",
        lambda: TIMESTAMP,
    )


@pytest.fixture
def patch_check_tcp_ports(monkeypatch, open_ports_data):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.tcp_scanner._check_tcp_ports",
        lambda *_: (TIMESTAMP, open_ports_data),
    )


def _get_tcp_scan_event(port_scan_data: PortScanData):
    port_statuses = {port: psd.status for port, psd in port_scan_data.items()}

    return TCPScanEvent(
        source=AGENT_ID,
        target=HOST_IP,
        timestamp=TIMESTAMP,
        ports=port_statuses,
    )


@pytest.mark.parametrize("open_ports_data", [OPEN_PORTS_DATA])
def test_tcp_successful(
    monkeypatch, patch_check_tcp_ports, open_ports_data, mock_agent_event_queue
):
    closed_ports = [8080, 143, 445]

    port_scan_data = scan_tcp_ports(HOST_IP, PORTS_TO_SCAN, 0, mock_agent_event_queue, AGENT_ID)

    assert len(port_scan_data) == 6
    for port in open_ports_data.keys():
        assert port_scan_data[port].port == port
        assert port_scan_data[port].status == PortStatus.OPEN
        assert port_scan_data[port].banner == open_ports_data.get(port)

    for port in closed_ports:
        assert port_scan_data[port].port == port
        assert port_scan_data[port].status == PortStatus.CLOSED
        assert port_scan_data[port].banner is None

    event = _get_tcp_scan_event(port_scan_data)

    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.mark.parametrize("open_ports_data", [{}])
def test_tcp_empty_response(
    monkeypatch, patch_check_tcp_ports, open_ports_data, mock_agent_event_queue
):
    port_scan_data = scan_tcp_ports(HOST_IP, PORTS_TO_SCAN, 0, mock_agent_event_queue, AGENT_ID)

    assert len(port_scan_data) == 6
    for port in open_ports_data:
        assert port_scan_data[port].port == port
        assert port_scan_data[port].status == PortStatus.CLOSED
        assert port_scan_data[port].banner is None

    event = _get_tcp_scan_event(port_scan_data)

    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.mark.parametrize("open_ports_data", [OPEN_PORTS_DATA])
def test_tcp_no_ports_to_scan(
    monkeypatch, patch_check_tcp_ports, open_ports_data, mock_agent_event_queue
):
    port_scan_data = scan_tcp_ports(HOST_IP, [], 0, mock_agent_event_queue, AGENT_ID)

    assert len(port_scan_data) == 0

    event = _get_tcp_scan_event(port_scan_data)

    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


def test_exception_handling(monkeypatch, mock_agent_event_queue):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.tcp_scanner._scan_tcp_ports",
        MagicMock(side_effect=Exception),
    )
    assert scan_tcp_ports("abc", [123], 123, mock_agent_event_queue, AGENT_ID) == EMPTY_PORT_SCAN
    assert mock_agent_event_queue.publish.call_count == 0
