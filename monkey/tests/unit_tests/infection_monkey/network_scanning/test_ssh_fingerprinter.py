import pytest

from common import OperatingSystem
from common.types import PortStatus
from infection_monkey.i_puppet import FingerprintData, PortScanData
from infection_monkey.network_scanning.ssh_fingerprinter import SSHFingerprinter


@pytest.fixture
def ssh_fingerprinter():
    return SSHFingerprinter()


def test_no_ssh_ports_open(ssh_fingerprinter):
    port_scan_data = {
        22: PortScanData(22, PortStatus.CLOSED, "", "tcp-22"),
        123: PortScanData(123, PortStatus.OPEN, "", "tcp-123"),
        443: PortScanData(443, PortStatus.CLOSED, "", "tcp-443"),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(None, None, {})


def test_no_os(ssh_fingerprinter):
    port_scan_data = {
        22: PortScanData(22, PortStatus.OPEN, "SSH-2.0-OpenSSH_8.2p1", "tcp-22"),
        2222: PortScanData(2222, PortStatus.OPEN, "SSH-2.0-OpenSSH_8.2p1", "tcp-2222"),
        443: PortScanData(443, PortStatus.CLOSED, "", "tcp-443"),
        8080: PortScanData(8080, PortStatus.CLOSED, "", "tcp-8080"),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(
        None,
        None,
        {
            "tcp-22": {
                "display_name": "SSH",
                "port": 22,
                "name": "ssh",
            },
            "tcp-2222": {
                "display_name": "SSH",
                "port": 2222,
                "name": "ssh",
            },
        },
    )


def test_ssh_os(ssh_fingerprinter):
    port_scan_data = {
        22: PortScanData(22, PortStatus.OPEN, "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2", "tcp-22"),
        443: PortScanData(443, PortStatus.CLOSED, "", "tcp-443"),
        8080: PortScanData(8080, PortStatus.CLOSED, "", "tcp-8080"),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(
        OperatingSystem.LINUX,
        "Ubuntu-4ubuntu0.2",
        {
            "tcp-22": {
                "display_name": "SSH",
                "port": 22,
                "name": "ssh",
            }
        },
    )


def test_multiple_os(ssh_fingerprinter):
    port_scan_data = {
        22: PortScanData(22, PortStatus.OPEN, "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2", "tcp-22"),
        2222: PortScanData(2222, PortStatus.OPEN, "SSH-2.0-OpenSSH_8.2p1 Debian", "tcp-2222"),
        443: PortScanData(443, PortStatus.CLOSED, "", "tcp-443"),
        8080: PortScanData(8080, PortStatus.CLOSED, "", "tcp-8080"),
    }
    results = ssh_fingerprinter.get_host_fingerprint("127.0.0.1", None, port_scan_data, None)

    assert results == FingerprintData(
        OperatingSystem.LINUX,
        "Debian",
        {
            "tcp-22": {
                "display_name": "SSH",
                "port": 22,
                "name": "ssh",
            },
            "tcp-2222": {
                "display_name": "SSH",
                "port": 2222,
                "name": "ssh",
            },
        },
    )
