from threading import Barrier, Event
from unittest.mock import MagicMock

import pytest

from infection_monkey.i_puppet import PortScanData
from infection_monkey.master import IPScanner
from infection_monkey.puppet.mock_puppet import MockPuppet

WINDOWS_OS = {"type": "windows"}
LINUX_OS = {"type": "linux"}


class MockPuppet(MockPuppet):
    def __init__(self):
        self.ping = MagicMock(side_effect=super().ping)
        self.scan_tcp_port = MagicMock(side_effect=super().scan_tcp_port)


@pytest.fixture
def scan_config():
    return {
        "tcp": {
            "timeout_ms": 3000,
            "ports": [
                22,
                445,
                3389,
                443,
                8008,
                3306,
            ],
        },
        "icmp": {
            "timeout_ms": 1000,
        },
    }


@pytest.fixture
def stop():
    return Event()


@pytest.fixture
def callback():
    return MagicMock()


def assert_dot_1(victim_host):
    assert victim_host.icmp is True
    assert victim_host.os == WINDOWS_OS

    assert len(victim_host.services.keys()) == 2
    assert "tcp-445" in victim_host.services
    assert victim_host.services["tcp-445"]["port"] == 445
    assert victim_host.services["tcp-445"]["banner"] == "SMB BANNER"
    assert "tcp-3389" in victim_host.services
    assert victim_host.services["tcp-3389"]["port"] == 3389


def assert_dot_3(victim_host):
    assert victim_host.icmp is True
    assert victim_host.os == LINUX_OS

    assert len(victim_host.services.keys()) == 2
    assert "tcp-22" in victim_host.services
    assert victim_host.services["tcp-22"]["port"] == 22
    assert victim_host.services["tcp-22"]["banner"] == "SSH BANNER"

    assert "tcp-443" in victim_host.services
    assert victim_host.services["tcp-443"]["port"] == 443
    assert victim_host.services["tcp-443"]["banner"] == "HTTPS BANNER"


def assert_host_down(victim_host):
    assert victim_host.icmp is False
    assert len(victim_host.services.keys()) == 0


def test_scan_single_ip(callback, scan_config, stop):
    ips = ["10.0.0.1"]

    ns = IPScanner(MockPuppet(), num_workers=1)
    ns.scan(ips, scan_config, callback, stop)

    callback.assert_called_once()

    assert_dot_1(callback.call_args_list[0][0][0])


def test_scan_multiple_ips(callback, scan_config, stop):
    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]

    ns = IPScanner(MockPuppet(), num_workers=4)
    ns.scan(ips, scan_config, callback, stop)

    assert callback.call_count == 4

    assert_dot_1(callback.call_args_list[0][0][0])
    assert_host_down(callback.call_args_list[1][0][0])
    assert_dot_3(callback.call_args_list[2][0][0])
    assert_host_down(callback.call_args_list[3][0][0])


def test_scan_lots_of_ips(callback, scan_config, stop):
    ips = [f"10.0.0.{i}" for i in range(0, 255)]

    ns = IPScanner(MockPuppet(), num_workers=4)
    ns.scan(ips, scan_config, callback, stop)

    assert callback.call_count == 255


def test_stop_after_callback(scan_config, stop):
    def _callback(_):
        # Block all threads here until 2 threads reach this barrier, then set stop
        # and test that niether thread continues to scan.
        _callback.barrier.wait()
        stop.set()

    _callback.barrier = Barrier(2)

    stopable_callback = MagicMock(side_effect=_callback)

    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]

    ns = IPScanner(MockPuppet(), num_workers=2)
    ns.scan(ips, scan_config, stopable_callback, stop)

    assert stopable_callback.call_count == 2


def test_interrupt_port_scanning(callback, scan_config, stop):
    def stopable_scan_tcp_port(port, _, __):
        # Block all threads here until 2 threads reach this barrier, then set stop
        # and test that niether thread scans any more ports
        stopable_scan_tcp_port.barrier.wait()
        stop.set()

        return PortScanData(port, False, None, None)

    stopable_scan_tcp_port.barrier = Barrier(2)

    puppet = MockPuppet()
    puppet.scan_tcp_port = MagicMock(side_effect=stopable_scan_tcp_port)

    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]

    ns = IPScanner(puppet, num_workers=2)
    ns.scan(ips, scan_config, callback, stop)

    assert puppet.scan_tcp_port.call_count == 2
