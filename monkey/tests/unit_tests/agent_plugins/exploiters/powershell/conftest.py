from unittest.mock import MagicMock

import pytest
from monkeytypes import NetworkProtocol, OperatingSystem, PortStatus

from common.types import NetworkPort
from infection_monkey.i_puppet import PortScanData, TargetHostPorts


def _create_windows_host(http_enabled, https_enabled):
    no_ssl_enabled_port = NetworkPort(5985)
    ssl_enabled_port = NetworkPort(5986)

    host = MagicMock()
    host.operating_system = OperatingSystem.WINDOWS
    host.ports_status = TargetHostPorts()

    if http_enabled:
        host.ports_status.tcp_ports[no_ssl_enabled_port] = PortScanData(
            port=no_ssl_enabled_port, status=PortStatus.OPEN, protocol=NetworkProtocol.TCP
        )

    if https_enabled:
        host.ports_status.tcp_ports[ssl_enabled_port] = PortScanData(
            port=ssl_enabled_port, status=PortStatus.OPEN, protocol=NetworkProtocol.TCP
        )

    return host


@pytest.fixture
def https_only_host():
    return _create_windows_host(False, True)


@pytest.fixture
def http_only_host():
    return _create_windows_host(True, False)


@pytest.fixture
def http_and_https_both_enabled_host():
    return _create_windows_host(True, True)


@pytest.fixture
def powershell_disabled_host():
    return _create_windows_host(False, False)
