from http import HTTPMethod
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.monkey_island.cc.models.test_agent import AGENT_ID

from common.event_queue import IAgentEventPublisher
from common.types import DiscoveredService, NetworkPort, NetworkProtocol, NetworkService, PortStatus
from infection_monkey.i_puppet import PortScanData
from infection_monkey.network_scanning.http_fingerprinter import HTTPFingerprinter

OPTIONS = {"http_ports": [80, 443, 1080, 8080, 9200]}

PYTHON_SERVER_HEADER = {"Server": "SimpleHTTP/0.6 Python/3.6.9"}
APACHE_SERVER_HEADER = {"Server": "Apache/Server/Header"}
NO_SERVER_HEADER = {"Not_Server": "No Header for you"}

SERVER_HEADERS = {
    "https://127.0.0.1:443": PYTHON_SERVER_HEADER,
    "http://127.0.0.1:8080": APACHE_SERVER_HEADER,
    "http://127.0.0.1:1080": NO_SERVER_HEADER,
}


@pytest.fixture
def mock_get_http_headers():
    return MagicMock(side_effect=lambda url: SERVER_HEADERS.get(url, None))


@pytest.fixture(autouse=True)
def patch_get_http_headers(monkeypatch, mock_get_http_headers):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.http_fingerprinter._get_http_headers",
        mock_get_http_headers,
    )


@pytest.fixture
def mock_agent_event_publisher() -> IAgentEventPublisher:
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def http_fingerprinter(mock_agent_event_publisher):
    return HTTPFingerprinter(AGENT_ID, mock_agent_event_publisher)


def test_no_http_ports_open(mock_get_http_headers, mock_agent_event_publisher, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(
            port=80, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
        123: PortScanData(
            port=123, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN
        ),
        443: PortScanData(
            port=443, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTPS
        ),
        8080: PortScanData(
            port=8080, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
    }
    http_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, OPTIONS)

    assert not mock_get_http_headers.called
    assert mock_agent_event_publisher.publish.call_count == 0


def test_fingerprint_only_port_443(
    mock_get_http_headers, mock_agent_event_publisher, http_fingerprinter
):
    port_scan_data = {
        80: PortScanData(
            port=80, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
        123: PortScanData(
            port=123, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN
        ),
        443: PortScanData(
            port=443, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN  # HTTPS
        ),
        8080: PortScanData(
            port=8080, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 1
    mock_get_http_headers.assert_called_with("https://127.0.0.1:443")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 1

    assert fingerprint_data.services[0].protocol == NetworkProtocol.TCP
    assert fingerprint_data.services[0].port == 443
    assert fingerprint_data.services[0].service == NetworkService.HTTPS

    assert mock_agent_event_publisher.publish.call_count == 1 + 1
    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].method == HTTPMethod.HEAD
    assert "443" in mock_agent_event_publisher.publish.call_args_list[0][0][0].url

    assert len(mock_agent_event_publisher.publish.call_args_list[1][0][0].discovered_services) == 1
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP, port=NetworkPort(443), service=NetworkService.HTTPS
        )
        in mock_agent_event_publisher.publish.call_args_list[1][0][0].discovered_services
    )


def test_open_port_no_http_server(
    mock_get_http_headers, mock_agent_event_publisher, http_fingerprinter
):
    port_scan_data = {
        80: PortScanData(
            port=80, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
        123: PortScanData(
            port=123, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN
        ),
        443: PortScanData(
            port=443, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTPS
        ),
        9200: PortScanData(
            port=9200, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 2
    mock_get_http_headers.assert_any_call("https://127.0.0.1:9200")
    mock_get_http_headers.assert_any_call("http://127.0.0.1:9200")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 0

    assert mock_agent_event_publisher.publish.call_count == 2 + 1

    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].method == HTTPMethod.HEAD
    assert "9200" in mock_agent_event_publisher.publish.call_args_list[0][0][0].url
    assert mock_agent_event_publisher.publish.call_args_list[1][0][0].method == HTTPMethod.HEAD
    assert "9200" in mock_agent_event_publisher.publish.call_args_list[1][0][0].url

    assert len(mock_agent_event_publisher.publish.call_args_list[2][0][0].discovered_services) == 0


def test_multiple_open_ports(mock_get_http_headers, mock_agent_event_publisher, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(
            port=80, status=PortStatus.CLOSED, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
        443: PortScanData(
            port=443, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN  # HTTPS
        ),
        8080: PortScanData(
            port=8080, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 3
    mock_get_http_headers.assert_any_call("https://127.0.0.1:443")
    mock_get_http_headers.assert_any_call("https://127.0.0.1:8080")
    mock_get_http_headers.assert_any_call("http://127.0.0.1:8080")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 2

    assert fingerprint_data.services[0].protocol == NetworkProtocol.TCP
    assert fingerprint_data.services[0].port == 443
    assert fingerprint_data.services[0].service == NetworkService.HTTPS

    assert fingerprint_data.services[1].protocol == NetworkProtocol.TCP
    assert fingerprint_data.services[1].port == 8080
    assert fingerprint_data.services[1].service == NetworkService.HTTP

    assert mock_agent_event_publisher.publish.call_count == 3 + 1

    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].method == HTTPMethod.HEAD
    assert "443" in mock_agent_event_publisher.publish.call_args_list[0][0][0].url
    assert mock_agent_event_publisher.publish.call_args_list[1][0][0].method == HTTPMethod.HEAD
    assert "8080" in mock_agent_event_publisher.publish.call_args_list[1][0][0].url
    assert mock_agent_event_publisher.publish.call_args_list[2][0][0].method == HTTPMethod.HEAD
    assert "8080" in mock_agent_event_publisher.publish.call_args_list[2][0][0].url

    assert len(mock_agent_event_publisher.publish.call_args_list[3][0][0].discovered_services) == 2
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP, port=NetworkPort(443), service=NetworkService.HTTPS
        )
        in mock_agent_event_publisher.publish.call_args_list[3][0][0].discovered_services
    )
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP, port=NetworkPort(8080), service=NetworkService.HTTP
        )
        in mock_agent_event_publisher.publish.call_args_list[3][0][0].discovered_services
    )


def test_server_missing_from_http_headers(
    mock_get_http_headers, mock_agent_event_publisher, http_fingerprinter
):
    port_scan_data = {
        1080: PortScanData(
            port=1080, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN  # HTTP
        ),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 2

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 1

    assert fingerprint_data.services[0].protocol == NetworkProtocol.TCP
    assert fingerprint_data.services[0].port == 1080
    assert fingerprint_data.services[0].service == NetworkService.HTTP

    assert mock_agent_event_publisher.publish.call_count == 2 + 1

    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].method == HTTPMethod.HEAD
    assert "1080" in mock_agent_event_publisher.publish.call_args_list[0][0][0].url
    assert mock_agent_event_publisher.publish.call_args_list[1][0][0].method == HTTPMethod.HEAD
    assert "1080" in mock_agent_event_publisher.publish.call_args_list[1][0][0].url

    assert len(mock_agent_event_publisher.publish.call_args_list[2][0][0].discovered_services) == 1
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP, port=NetworkPort(1080), service=NetworkService.HTTP
        )
        in mock_agent_event_publisher.publish.call_args_list[2][0][0].discovered_services
    )
