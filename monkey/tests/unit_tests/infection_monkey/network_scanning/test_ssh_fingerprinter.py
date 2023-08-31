import pytest

from common import OperatingSystem
from common.types import DiscoveredService, NetworkProtocol, NetworkService, PortStatus
from infection_monkey.i_puppet import FingerprintData, PortScanData
from infection_monkey.network_scanning.ssh_fingerprinter import SSHFingerprinter

SSH_SERVICE_22 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=22, service=NetworkService.SSH
)

SSH_SERVICE_2222 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=2222, service=NetworkService.SSH
)


@pytest.fixture
def ssh_fingerprinter():
    return SSHFingerprinter()


def test_no_ssh_ports_open(ssh_fingerprinter):
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


def test_no_os(ssh_fingerprinter):
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


def test_ssh_os(ssh_fingerprinter):
    port_scan_data = {
        22: PortScanData(
            port=22,
            status=PortStatus.OPEN,
            banner="SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2",
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
        os_type=OperatingSystem.LINUX, os_version="Ubuntu-4ubuntu0.2", services=[SSH_SERVICE_22]
    )


def test_multiple_os(ssh_fingerprinter):
    port_scan_data = {
        22: PortScanData(
            port=22,
            status=PortStatus.OPEN,
            banner="SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2",
            service=NetworkService.SSH,
        ),
        2222: PortScanData(
            port=2222,
            status=PortStatus.OPEN,
            banner="SSH-2.0-OpenSSH_8.2p1 Debian",
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
        os_type=OperatingSystem.LINUX,
        os_version="Debian",
        services=[SSH_SERVICE_22, SSH_SERVICE_2222],
    )
