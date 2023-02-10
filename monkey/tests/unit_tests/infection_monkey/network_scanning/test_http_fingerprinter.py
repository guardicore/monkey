from unittest.mock import MagicMock

import pytest

from common.types import PortStatus
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
def http_fingerprinter():
    return HTTPFingerprinter()


def test_no_http_ports_open(mock_get_http_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(port=80, status=PortStatus.CLOSED, banner="", service="tcp-80"),
        123: PortScanData(port=123, status=PortStatus.OPEN, banner="", service="tcp-123"),
        443: PortScanData(port=443, status=PortStatus.CLOSED, banner="", service="tcp-443"),
        8080: PortScanData(port=8080, status=PortStatus.CLOSED, banner="", service="tcp-8080"),
    }
    http_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, OPTIONS)

    assert not mock_get_http_headers.called


def test_fingerprint_only_port_443(mock_get_http_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(port=80, status=PortStatus.CLOSED, banner="", service="tcp-80"),
        123: PortScanData(port=123, status=PortStatus.OPEN, banner="", service="tcp-123"),
        443: PortScanData(port=443, status=PortStatus.OPEN, banner="", service="tcp-443"),
        8080: PortScanData(port=8080, status=PortStatus.CLOSED, banner="", service="tcp-8080"),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 1
    mock_get_http_headers.assert_called_with("https://127.0.0.1:443")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 1

    assert fingerprint_data.services["tcp-443"]["data"][0] == PYTHON_SERVER_HEADER["Server"]
    assert fingerprint_data.services["tcp-443"]["data"][1] is True


def test_open_port_no_http_server(mock_get_http_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(port=80, status=PortStatus.CLOSED, banner="", service="tcp-80"),
        123: PortScanData(port=123, status=PortStatus.OPEN, banner="", service="tcp-123"),
        443: PortScanData(port=443, status=PortStatus.CLOSED, banner="", service="tcp-443"),
        9200: PortScanData(port=9200, status=PortStatus.OPEN, banner="", service="tcp-9200"),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 2
    mock_get_http_headers.assert_any_call("https://127.0.0.1:9200")
    mock_get_http_headers.assert_any_call("http://127.0.0.1:9200")

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 0


def test_multiple_open_ports(mock_get_http_headers, http_fingerprinter):
    port_scan_data = {
        80: PortScanData(port=80, status=PortStatus.CLOSED, banner="", service="tcp-80"),
        443: PortScanData(port=443, status=PortStatus.OPEN, banner="", service="tcp-443"),
        8080: PortScanData(port=8080, status=PortStatus.OPEN, banner="", service="tcp-8080"),
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
    assert len(fingerprint_data.services.keys()) == 2

    assert fingerprint_data.services["tcp-443"]["data"][0] == PYTHON_SERVER_HEADER["Server"]
    assert fingerprint_data.services["tcp-443"]["data"][1] is True
    assert fingerprint_data.services["tcp-8080"]["data"][0] == APACHE_SERVER_HEADER["Server"]
    assert fingerprint_data.services["tcp-8080"]["data"][1] is False


def test_server_missing_from_http_headers(mock_get_http_headers, http_fingerprinter):
    port_scan_data = {
        1080: PortScanData(port=1080, status=PortStatus.OPEN, banner="", service="tcp-1080"),
    }
    fingerprint_data = http_fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, port_scan_data, OPTIONS
    )

    assert mock_get_http_headers.call_count == 2

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 1

    assert fingerprint_data.services["tcp-1080"]["data"][0] == ""
    assert fingerprint_data.services["tcp-1080"]["data"][1] is False
