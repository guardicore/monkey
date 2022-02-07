from unittest.mock import MagicMock

import pytest

from infection_monkey.i_puppet import PortScanData, PortStatus
from infection_monkey.network.http_fingerprinter import HTTPFingerprinter

OPTIONS = {"http_ports": [80, 443, 8080, 9200]}

PYTHON_SERVER_HEADER = "SimpleHTTP/0.6 Python/3.6.9"
APACHE_SERVER_HEADER = "Apache/Server/Header"

SERVER_HEADERS = {
    "https://127.0.0.1:443": PYTHON_SERVER_HEADER,
    "http://127.0.0.1:8080": APACHE_SERVER_HEADER,
}


@pytest.fixture
def mock_get_server_from_headers():
    return MagicMock(side_effect=lambda port: SERVER_HEADERS.get(port, None))


@pytest.fixture(autouse=True)
def patch_get_server_from_headers(monkeypatch, mock_get_server_from_headers):
    monkeypatch.setattr(
        "infection_monkey.network.http_fingerprinter._get_server_from_headers",
        mock_get_server_from_headers,
    )


@pytest.fixture
def http_fingerprinter():
    return HTTPFingerprinter()


def test_no_http_ports_open(mock_get_server_from_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(80, PortStatus.CLOSED, "", "tcp-80"),
        123: PortScanData(123, PortStatus.OPEN, "", "tcp-123"),
        443: PortScanData(443, PortStatus.CLOSED, "", "tcp-443"),
        8080: PortScanData(8080, PortStatus.CLOSED, "", "tcp-8080"),
    }
    http_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, OPTIONS)

    assert not mock_get_server_from_headers.called


def test_fingerprint_only_port_443(mock_get_server_from_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(80, PortStatus.CLOSED, "", "tcp-80"),
        123: PortScanData(123, PortStatus.OPEN, "", "tcp-123"),
        443: PortScanData(443, PortStatus.OPEN, "", "tcp-443"),
        8080: PortScanData(8080, PortStatus.CLOSED, "", "tcp-8080"),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_server_from_headers.call_count == 1
    mock_get_server_from_headers.assert_called_with("https://127.0.0.1:443")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 1

    assert fingerprint_data.services["tcp-443"]["data"][0] == PYTHON_SERVER_HEADER
    assert fingerprint_data.services["tcp-443"]["data"][1] is True


def test_open_port_no_http_server(mock_get_server_from_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(80, PortStatus.CLOSED, "", "tcp-80"),
        123: PortScanData(123, PortStatus.OPEN, "", "tcp-123"),
        443: PortScanData(443, PortStatus.CLOSED, "", "tcp-443"),
        9200: PortScanData(9200, PortStatus.OPEN, "", "tcp-9200"),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_server_from_headers.call_count == 2
    mock_get_server_from_headers.assert_any_call("https://127.0.0.1:9200")
    mock_get_server_from_headers.assert_any_call("http://127.0.0.1:9200")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 0


def test_multiple_open_ports(mock_get_server_from_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(80, PortStatus.CLOSED, "", "tcp-80"),
        443: PortScanData(443, PortStatus.OPEN, "", "tcp-443"),
        8080: PortScanData(8080, PortStatus.OPEN, "", "tcp-8080"),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_server_from_headers.call_count == 3
    mock_get_server_from_headers.assert_any_call("https://127.0.0.1:443")
    mock_get_server_from_headers.assert_any_call("https://127.0.0.1:8080")
    mock_get_server_from_headers.assert_any_call("http://127.0.0.1:8080")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 2

    assert fingerprint_data.services["tcp-443"]["data"][0] == PYTHON_SERVER_HEADER
    assert fingerprint_data.services["tcp-443"]["data"][1] is True
    assert fingerprint_data.services["tcp-8080"]["data"][0] == APACHE_SERVER_HEADER
    assert fingerprint_data.services["tcp-8080"]["data"][1] is False
