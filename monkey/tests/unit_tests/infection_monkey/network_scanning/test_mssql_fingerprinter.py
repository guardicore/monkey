import socket
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.monkey_island.cc.models.test_agent import AGENT_ID

from common.event_queue import IAgentEventPublisher
from common.types import DiscoveredService, NetworkPort, NetworkProtocol, NetworkService, PortStatus
from infection_monkey.i_puppet import PortScanData
from infection_monkey.network_scanning.mssql_fingerprinter import (
    SQL_BROWSER_DEFAULT_PORT,
    MSSQLFingerprinter,
)

PORT_SCAN_DATA_BOGUS = {
    80: PortScanData(port=80, status=PortStatus.OPEN, banner="", service=NetworkService.HTTP),
    8080: PortScanData(port=8080, status=PortStatus.OPEN, banner="", service=NetworkService.HTTPS),
}

MSSQL_DISCOVERED_SERVICE = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=NetworkPort(1433), service=NetworkService.MSSQL
)

SQL_BROWSER_DISCOVERED_SERVICE = DiscoveredService(
    protocol=NetworkProtocol.UDP,
    port=SQL_BROWSER_DEFAULT_PORT,
    service=NetworkService.MSSQL_BROWSER,
)


@pytest.fixture
def mock_agent_event_publisher() -> IAgentEventPublisher:
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def fingerprinter(mock_agent_event_publisher):
    return MSSQLFingerprinter(AGENT_ID, mock_agent_event_publisher)


def test_mssql_fingerprint_successful(monkeypatch, mock_agent_event_publisher, fingerprinter):
    successful_server_response = (
        b"\x05y\x00ServerName;BogusVogus;InstanceName;GhostServer;"
        b"IsClustered;No;Version;11.1.1111.111;tcp;1433;np;blah_blah;;"
    )
    monkeypatch.setattr(
        "infection_monkey.network_scanning.mssql_fingerprinter._query_mssql_for_instance_data",
        lambda _, __: successful_server_response,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_BOGUS, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 2

    expected_services = list(set([MSSQL_DISCOVERED_SERVICE, SQL_BROWSER_DISCOVERED_SERVICE]))
    assert fingerprint_data.services == expected_services

    assert mock_agent_event_publisher.publish.call_count == 1
    assert len(mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services) == 2
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP,
            port=NetworkPort(1433),  # taken from `successful_server_response`
            service=NetworkService.MSSQL,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.UDP,
            port=SQL_BROWSER_DEFAULT_PORT,
            service=NetworkService.MSSQL_BROWSER,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )


@pytest.mark.parametrize(
    "mock_query_function",
    [
        MagicMock(side_effect=socket.timeout),
        MagicMock(side_effect=socket.error),
        MagicMock(side_effect=Exception),
    ],
)
def test_mssql_no_response_from_server(
    monkeypatch, mock_agent_event_publisher, fingerprinter, mock_query_function
):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.mssql_fingerprinter._query_mssql_for_instance_data",
        mock_query_function,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_BOGUS, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 0

    assert mock_agent_event_publisher.publish.call_count == 1
    assert len(mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services) == 0


def test_mssql_wrong_response_from_server(monkeypatch, mock_agent_event_publisher, fingerprinter):
    mangled_server_response = (
        b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        b"Pellentesque ultrices ornare libero, ;;"
    )
    monkeypatch.setattr(
        "infection_monkey.network_scanning.mssql_fingerprinter.socket.socket.recvfrom",
        lambda _, __: (mangled_server_response, _),
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_BOGUS, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services) == 1

    assert fingerprint_data.services[0].service == NetworkService.UNKNOWN
    assert fingerprint_data.services[0].port == SQL_BROWSER_DEFAULT_PORT
    assert fingerprint_data.services[0].protocol == NetworkProtocol.UDP

    assert mock_agent_event_publisher.publish.call_count == 1
    assert len(mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services) == 1
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.UDP,
            port=SQL_BROWSER_DEFAULT_PORT,
            service=NetworkService.UNKNOWN,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )
