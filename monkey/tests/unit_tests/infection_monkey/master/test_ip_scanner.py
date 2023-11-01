from threading import Barrier, Event
from typing import Set
from unittest.mock import MagicMock

import pytest
from monkeytypes import NetworkProtocol, NetworkService, OperatingSystem, PortStatus
from tests.unit_tests.infection_monkey.master.mock_puppet import MockPuppet
from tests.utils import ThreadSafeMagicMock

from common.agent_configuration.agent_sub_configurations import (
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    TCPScanConfiguration,
)
from infection_monkey.i_puppet import FingerprintData, PingScanData, PortScanData
from infection_monkey.master import IPScanner
from infection_monkey.network import NetworkAddress

WINDOWS_OS = OperatingSystem.WINDOWS
LINUX_OS = OperatingSystem.LINUX


@pytest.fixture
def scan_config(default_agent_configuration):
    tcp_config = TCPScanConfiguration(
        timeout=3,
        ports=[
            22,
            445,
            3389,
            443,
            8008,
            3306,
        ],
    )
    icmp_config = ICMPScanConfiguration(timeout=1)
    fingerprinter_config = {
        "HTTPFinger": {},
        "SMBFinger": {},
        "SSHFinger": {},
    }
    scan_config = NetworkScanConfiguration(
        tcp=tcp_config,
        icmp=icmp_config,
        fingerprinters=fingerprinter_config,
        targets=default_agent_configuration.propagation.network_scan.targets,
    )
    return scan_config


@pytest.fixture
def stop():
    return Event()


@pytest.fixture
def callback():
    return ThreadSafeMagicMock()


def assert_port_status(port_scan_data, expected_open_ports: Set[int]):
    for psd in port_scan_data.values():
        if psd.port in expected_open_ports:
            assert psd.status == PortStatus.OPEN
        else:
            assert psd.status == PortStatus.CLOSED


def assert_scan_results(address, scan_results):
    ping_scan_data = scan_results.ping_scan_data
    port_scan_data = scan_results.port_scan_data
    fingerprint_data = scan_results.fingerprint_data

    if address.ip == "10.0.0.1":
        assert_scan_results_no_1(address.domain, ping_scan_data, port_scan_data, fingerprint_data)
    elif address.ip == "10.0.0.3":
        assert_scan_results_no_3(address.domain, ping_scan_data, port_scan_data, fingerprint_data)
    else:
        assert_scan_results_host_down(address, ping_scan_data, port_scan_data, fingerprint_data)


def assert_scan_results_no_1(
    domain,
    ping_scan_data: PingScanData,
    port_scan_data: PortScanData,
    fingerprint_data: FingerprintData,
):
    assert domain == "d1"
    assert ping_scan_data.response_received is True
    assert ping_scan_data.os == OperatingSystem.WINDOWS

    assert len(port_scan_data.keys()) == 6

    psd_445 = port_scan_data[445]
    psd_3389 = port_scan_data[3389]

    assert psd_445.port == 445
    assert psd_445.banner == "SMB BANNER"
    assert psd_445.service == NetworkService.SMB

    assert psd_3389.port == 3389
    assert psd_3389.banner == ""
    assert psd_3389.service == NetworkService.UNKNOWN

    assert_port_status(port_scan_data, {445, 3389})
    assert_fingerprint_results_no_1(fingerprint_data)


def assert_fingerprint_results_no_1(fingerprint_data: FingerprintData):
    assert len(fingerprint_data.keys()) == 3
    assert fingerprint_data["SSHFinger"].services == []
    assert fingerprint_data["HTTPFinger"].services == []

    assert fingerprint_data["SMBFinger"].os_type == OperatingSystem.WINDOWS
    assert fingerprint_data["SMBFinger"].os_version == "vista"

    assert len(fingerprint_data["SMBFinger"].services) == 1
    assert fingerprint_data["SMBFinger"].services[0].port == 445
    assert fingerprint_data["SMBFinger"].services[0].protocol == NetworkProtocol.TCP
    assert fingerprint_data["SMBFinger"].services[0].service == NetworkService.SMB


def assert_scan_results_no_3(
    domain,
    ping_scan_data: PingScanData,
    port_scan_data: PortScanData,
    fingerprint_data: FingerprintData,
):
    assert domain == "d3"

    assert ping_scan_data.response_received is True
    assert ping_scan_data.os == OperatingSystem.LINUX
    assert len(port_scan_data.keys()) == 6

    psd_443 = port_scan_data[443]
    psd_22 = port_scan_data[22]

    assert psd_443.port == 443
    assert psd_443.banner == "HTTPS BANNER"
    assert psd_443.service == NetworkService.HTTPS

    assert psd_22.port == 22
    assert psd_22.banner == "SSH BANNER"
    assert psd_22.service == NetworkService.SSH

    assert_port_status(port_scan_data, {22, 443})
    assert_fingerprint_results_no_3(fingerprint_data)


def assert_fingerprint_results_no_3(fingerprint_data: FingerprintData):
    assert len(fingerprint_data.keys()) == 3
    assert fingerprint_data["SMBFinger"].services == []

    assert fingerprint_data["SSHFinger"].os_type == OperatingSystem.LINUX
    assert fingerprint_data["SSHFinger"].os_version == "ubuntu"

    assert len(fingerprint_data["SSHFinger"].services) == 1
    assert fingerprint_data["SSHFinger"].services[0].port == 22
    assert fingerprint_data["SSHFinger"].services[0].protocol == NetworkProtocol.TCP
    assert fingerprint_data["SSHFinger"].services[0].service == NetworkService.SSH

    assert len(fingerprint_data["HTTPFinger"].services) == 2
    assert fingerprint_data["HTTPFinger"].services[0].port == 80
    assert fingerprint_data["HTTPFinger"].services[0].protocol == NetworkProtocol.TCP
    assert fingerprint_data["HTTPFinger"].services[0].service == NetworkService.HTTP

    assert fingerprint_data["HTTPFinger"].services[1].port == 443
    assert fingerprint_data["HTTPFinger"].services[1].protocol == NetworkProtocol.TCP
    assert fingerprint_data["HTTPFinger"].services[1].service == NetworkService.HTTPS


def assert_scan_results_host_down(
    address,
    ping_scan_data: PingScanData,
    port_scan_data: PortScanData,
    fingerprint_data: FingerprintData,
):
    assert address.ip not in {"10.0.0.1", "10.0.0.3"}
    assert address.domain is None

    assert ping_scan_data.response_received is False
    assert len(port_scan_data.keys()) == 6
    assert_port_status(port_scan_data, set())

    assert fingerprint_data == {}


def test_scan_single_ip(callback, scan_config, stop):
    addresses = [NetworkAddress("10.0.0.1", "d1")]

    ns = IPScanner(MockPuppet(), num_workers=1)
    ns.scan(addresses, scan_config, callback, stop)

    callback.assert_called_once()

    (address, scan_results) = callback.call_args_list[0][0]
    assert_scan_results(address, scan_results)


def test_scan_multiple_ips(callback, scan_config, stop):
    addresses = [
        NetworkAddress("10.0.0.1", "d1"),
        NetworkAddress("10.0.0.2", None),
        NetworkAddress("10.0.0.3", "d3"),
        NetworkAddress("10.0.0.4", None),
    ]

    ns = IPScanner(MockPuppet(), num_workers=4)
    ns.scan(addresses, scan_config, callback, stop)

    assert callback.call_count == 4

    (address, scan_results) = callback.call_args_list[0][0]
    assert_scan_results(address, scan_results)

    (address, scan_results) = callback.call_args_list[1][0]
    assert_scan_results(address, scan_results)

    (address, scan_results) = callback.call_args_list[2][0]
    assert_scan_results(address, scan_results)

    (address, scan_results) = callback.call_args_list[3][0]
    assert_scan_results(address, scan_results)


@pytest.mark.slow
def test_scan_lots_of_ips(callback, scan_config, stop):
    addresses = [NetworkAddress(f"10.0.0.{i}", None) for i in range(0, 255)]

    ns = IPScanner(MockPuppet(), num_workers=4)
    ns.scan(addresses, scan_config, callback, stop)

    assert callback.call_count == 255


def test_stop_after_callback(scan_config, stop):
    def _callback(*_):
        # Block all threads here until 2 threads reach this barrier, then set stop
        # and test that neither thread continues to scan.
        _callback.barrier.wait()
        stop.set()

    _callback.barrier = Barrier(2)

    stoppable_callback = MagicMock(side_effect=_callback)

    addresses = [
        NetworkAddress("10.0.0.1", None),
        NetworkAddress("10.0.0.2", None),
        NetworkAddress("10.0.0.3", None),
        NetworkAddress("10.0.0.4", None),
    ]

    ns = IPScanner(MockPuppet(), num_workers=2)
    ns.scan(addresses, scan_config, stoppable_callback, stop)

    assert stoppable_callback.call_count == 2


def test_interrupt_before_fingerprinting(callback, scan_config, stop):
    def stoppable_scan_tcp_ports(host_, ports, *_):
        # Block all threads here until 2 threads reach this barrier, then set stop
        # and test that neither thread scans any more ports
        stoppable_scan_tcp_ports.barrier.wait()
        stop.set()

        return {port: PortScanData(port=port, status=PortStatus.CLOSED) for port in ports}

    stoppable_scan_tcp_ports.barrier = Barrier(2)

    puppet = MockPuppet()
    puppet.scan_tcp_ports = MagicMock(side_effect=stoppable_scan_tcp_ports)
    puppet.fingerprint = MagicMock()

    addresses = [
        NetworkAddress("10.0.0.1", None),
        NetworkAddress("10.0.0.2", None),
        NetworkAddress("10.0.0.3", None),
        NetworkAddress("10.0.0.4", None),
    ]

    ns = IPScanner(puppet, num_workers=2)
    ns.scan(addresses, scan_config, callback, stop)

    puppet.fingerprint.assert_not_called()


def test_interrupt_fingerprinting(callback, scan_config, stop):
    def stoppable_fingerprint(*_):
        # Block all threads here until 2 threads reach this barrier, then set stop
        # and test that neither thread scans any more ports
        stoppable_fingerprint.barrier.wait()
        stop.set()

        return FingerprintData(os_type=None, os_version=None, services=[])

    stoppable_fingerprint.barrier = Barrier(2)

    puppet = MockPuppet()
    puppet.fingerprint = MagicMock(side_effect=stoppable_fingerprint)

    addresses = [
        NetworkAddress("10.0.0.1", None),
        NetworkAddress("10.0.0.2", None),
        NetworkAddress("10.0.0.3", None),
        NetworkAddress("10.0.0.4", None),
    ]

    ns = IPScanner(puppet, num_workers=2)
    ns.scan(addresses, scan_config, callback, stop)

    assert puppet.fingerprint.call_count == 2
