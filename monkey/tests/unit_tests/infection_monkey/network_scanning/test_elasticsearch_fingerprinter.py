from unittest.mock import MagicMock

import pytest

from common.common_consts.network_consts import ES_SERVICE
from common.types import PortStatus
from infection_monkey.i_puppet import PortScanData
from infection_monkey.network_scanning.elasticsearch_fingerprinter import (
    ES_PORT,
    ElasticSearchFingerprinter,
)

PORT_SCAN_DATA_OPEN = {ES_PORT: PortScanData(ES_PORT, PortStatus.OPEN, "", f"tcp-{ES_PORT}")}
PORT_SCAN_DATA_CLOSED = {ES_PORT: PortScanData(ES_PORT, PortStatus.CLOSED, "", f"tcp-{ES_PORT}")}
PORT_SCAN_DATA_MISSING = {
    80: PortScanData(80, PortStatus.OPEN, "", "tcp-80"),
    8080: PortScanData(8080, PortStatus.OPEN, "", "tcp-8080"),
}


@pytest.fixture
def fingerprinter():
    return ElasticSearchFingerprinter()


def test_successful(monkeypatch, fingerprinter):
    successful_server_response = {
        "cluster_name": "test cluster",
        "name": "test name",
        "version": {"number": "1.0.0"},
    }
    monkeypatch.setattr(
        "infection_monkey.network_scanning.elasticsearch_fingerprinter._query_elasticsearch",
        lambda _: successful_server_response,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_OPEN, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 1

    es_service = fingerprint_data.services[ES_SERVICE]

    assert es_service["cluster_name"] == successful_server_response["cluster_name"]
    assert es_service["version"] == successful_server_response["version"]["number"]
    assert es_service["name"] == successful_server_response["name"]


@pytest.mark.parametrize("port_scan_data", [PORT_SCAN_DATA_CLOSED, PORT_SCAN_DATA_MISSING])
def test_fingerprinting_skipped_if_port_closed(monkeypatch, fingerprinter, port_scan_data):
    mock_query_elasticsearch = MagicMock()
    monkeypatch.setattr(
        "infection_monkey.network_scanning.elasticsearch_fingerprinter._query_elasticsearch",
        mock_query_elasticsearch,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, {})

    assert not mock_query_elasticsearch.called
    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 0


@pytest.mark.parametrize(
    "mock_query_function",
    [
        MagicMock(side_effect=Exception("test exception")),
        MagicMock(return_value={"unexpected_key": "unexpected_value"}),
    ],
)
def test_no_response_from_server(monkeypatch, fingerprinter, mock_query_function):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.elasticsearch_fingerprinter._query_elasticsearch",
        mock_query_function,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_OPEN, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 0
