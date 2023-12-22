from unittest.mock import MagicMock

import pytest
from monkeytypes import (
    DiscoveredService,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    OperatingSystem,
    PortStatus,
)
from tests.unit_tests.monkey_island.cc.models.test_agent import AGENT_ID

from common.event_queue import IAgentEventPublisher
from infection_monkey.i_puppet import FingerprintData, PortScanData
from infection_monkey.network_scanning.ssh_fingerprinter import SSHFingerprinter

SSH_SERVICE_22 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=22, service=NetworkService.SSH
)

SSH_SERVICE_2222 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=2222, service=NetworkService.SSH
)


@pytest.fixture
def mock_agent_event_publisher() -> IAgentEventPublisher:
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def ssh_fingerprinter(mock_agent_event_publisher):
    return SSHFingerprinter(AGENT_ID, mock_agent_event_publisher)


def test_no_ssh_ports_open(ssh_fingerprinter, mock_agent_event_publisher):
    port_scan_data = {
        22: PortScanData(port=22, status=PortStatus.CLOSED, banner="", service=NetworkService.SSH),
        123: PortScanData(
            port=123, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN
        ),
        443: PortScanData(
            port=443, status=PortStatus.CLOSED, banner="", service=NetworkService.HTTPS
        ),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(os_type=None, os_version=None, services=[])

    assert mock_agent_event_publisher.publish.call_count == 0


def test_no_os(ssh_fingerprinter, mock_agent_event_publisher):
    port_scan_data = {
        22: PortScanData(
            port=22,
            status=PortStatus.OPEN,
            banner="SSH-2.0-OpenSSH_8.2p1",
            service=NetworkService.SSH,
        ),
        2222: PortScanData(
            port=2222,
            status=PortStatus.OPEN,
            banner="SSH-2.0-OpenSSH_8.2p1",
            service=NetworkService.SSH,
        ),
        443: PortScanData(
            port=443, status=PortStatus.CLOSED, banner="", service=NetworkService.HTTPS
        ),
        8080: PortScanData(
            port=8080, status=PortStatus.CLOSED, banner="", service=NetworkService.HTTP
        ),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(
        os_type=None,
        os_version=None,
        services=[SSH_SERVICE_22, SSH_SERVICE_2222],
    )

    assert mock_agent_event_publisher.publish.call_count == 1
    assert len(mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services) == 2
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP,
            port=NetworkPort(22),
            service=NetworkService.SSH,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP,
            port=NetworkPort(2222),
            service=NetworkService.SSH,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )
    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].os is None
    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].os_version is None


def test_ssh_os(ssh_fingerprinter, mock_agent_event_publisher):
    os_version = "Ubuntu-4ubuntu0.2"

    port_scan_data = {
        22: PortScanData(
            port=22,
            status=PortStatus.OPEN,
            banner=f"SSH-2.0-OpenSSH_8.2p1 {os_version}",
            service=NetworkService.SSH,
        ),
        443: PortScanData(
            port=443, status=PortStatus.CLOSED, banner="", service=NetworkService.HTTPS
        ),
        8080: PortScanData(
            port=8080, status=PortStatus.CLOSED, banner="", service=NetworkService.HTTP
        ),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(
        os_type=OperatingSystem.LINUX, os_version=os_version, services=[SSH_SERVICE_22]
    )

    assert mock_agent_event_publisher.publish.call_count == 1
    assert len(mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services) == 1
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP,
            port=NetworkPort(22),
            service=NetworkService.SSH,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )

    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].os is OperatingSystem.LINUX
    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].os_version == os_version


def test_os_info_not_overwritten(ssh_fingerprinter, mock_agent_event_publisher):
    os_version = "Ubuntu-4ubuntu0.2"

    port_scan_data = {
        22: PortScanData(
            port=22,
            status=PortStatus.OPEN,
            banner=f"SSH-2.0-OpenSSH_8.2p1 {os_version}",
            service=NetworkService.SSH,
        ),
        2222: PortScanData(
            port=2222,
            status=PortStatus.OPEN,
            banner="SSH-2.0-OpenSSH_8.2p1 OSThatShouldBeIgnored",
            service=NetworkService.SSH,
        ),
        8080: PortScanData(
            port=8080, status=PortStatus.CLOSED, banner="", service=NetworkService.HTTP
        ),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(
        os_type=OperatingSystem.LINUX,
        os_version=os_version,
        services=[SSH_SERVICE_22, SSH_SERVICE_2222],
    )

    assert mock_agent_event_publisher.publish.call_count == 1
    assert len(mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services) == 2
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP,
            port=NetworkPort(22),
            service=NetworkService.SSH,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )
    assert (
        DiscoveredService(
            protocol=NetworkProtocol.TCP,
            port=NetworkPort(2222),
            service=NetworkService.SSH,
        )
        in mock_agent_event_publisher.publish.call_args_list[0][0][0].discovered_services
    )

    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].os is OperatingSystem.LINUX
    assert mock_agent_event_publisher.publish.call_args_list[0][0][0].os_version == os_version
