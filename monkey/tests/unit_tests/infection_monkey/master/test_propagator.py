from ipaddress import IPv4Interface
from threading import Event
from unittest.mock import MagicMock

import pytest

from common import OperatingSystem
from common.agent_configuration.agent_sub_configurations import (
    NetworkScanConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
)
from common.types import PingScanData, PortStatus
from infection_monkey.i_puppet import ExploiterResultData, FingerprintData, PortScanData
from infection_monkey.master import IPScanResults, Propagator
from infection_monkey.model import TargetHost, TargetHostFactory
from infection_monkey.network import NetworkAddress


@pytest.fixture
def mock_target_host_factory():
    class MockTargetHostFactory(TargetHostFactory):
        def __init__(self):
            pass

        def build_target_host(self, network_address: NetworkAddress) -> TargetHost:
            domain = network_address.domain or ""
            return TargetHost(network_address.ip, domain)

    return MockTargetHostFactory()


empty_fingerprint_data = FingerprintData(None, None, {})

dot_1_scan_results = IPScanResults(
    PingScanData(True, OperatingSystem.WINDOWS),
    {
        22: PortScanData(22, PortStatus.CLOSED, None, None),
        445: PortScanData(445, PortStatus.OPEN, "SMB BANNER", "tcp-445"),
        3389: PortScanData(3389, PortStatus.OPEN, "", "tcp-3389"),
    },
    {
        "SMBFinger": FingerprintData("windows", "vista", {"tcp-445": {"name": "smb_service_name"}}),
        "SSHFinger": empty_fingerprint_data,
        "HTTPFinger": empty_fingerprint_data,
    },
)

dot_3_scan_results = IPScanResults(
    PingScanData(True, OperatingSystem.LINUX),
    {
        22: PortScanData(22, PortStatus.OPEN, "SSH BANNER", "tcp-22"),
        443: PortScanData(443, PortStatus.OPEN, "HTTPS BANNER", "tcp-443"),
        3389: PortScanData(3389, PortStatus.CLOSED, "", None),
    },
    {
        "SSHFinger": FingerprintData(
            "linux", "ubuntu", {"tcp-22": {"name": "SSH", "banner": "SSH BANNER"}}
        ),
        "HTTPFinger": FingerprintData(
            None,
            None,
            {
                "tcp-80": {"name": "http", "data": ("SERVER_HEADERS", False)},
                "tcp-443": {"name": "http", "data": ("SERVER_HEADERS_2", True)},
            },
        ),
        "SMBFinger": empty_fingerprint_data,
    },
)

dead_host_scan_results = IPScanResults(
    PingScanData(False, None),
    {
        22: PortScanData(22, PortStatus.CLOSED, None, None),
        443: PortScanData(443, PortStatus.CLOSED, None, None),
        3389: PortScanData(3389, PortStatus.CLOSED, "", None),
    },
    {},
)

dot_1_services = {
    "tcp-445": {
        "name": "smb_service_name",
        "display_name": "unknown(TCP)",
        "port": 445,
        "banner": "SMB BANNER",
    },
    "tcp-3389": {"display_name": "unknown(TCP)", "port": 3389, "banner": ""},
}

dot_3_services = {
    "tcp-22": {"name": "SSH", "display_name": "unknown(TCP)", "port": 22, "banner": "SSH BANNER"},
    "tcp-80": {"name": "http", "data": ("SERVER_HEADERS", False)},
    "tcp-443": {
        "name": "http",
        "display_name": "unknown(TCP)",
        "port": 443,
        "banner": "HTTPS BANNER",
        "data": ("SERVER_HEADERS_2", True),
    },
}

os_windows = "windows"

os_linux = "linux"

SERVERS = ["127.0.0.1:5000", "10.10.10.10:5007"]


@pytest.fixture
def mock_ip_scanner():
    def scan(adresses_to_scan, _, results_callback, stop):
        for address in adresses_to_scan:
            if address.ip.endswith(".1"):
                results_callback(address, dot_1_scan_results)
            elif address.ip.endswith(".3"):
                results_callback(address, dot_3_scan_results)
            else:
                results_callback(address, dead_host_scan_results)

    ip_scanner = MagicMock()
    ip_scanner.scan = MagicMock(side_effect=scan)

    return ip_scanner


class StubExploiter:
    def exploit_hosts(
        self,
        exploiters_to_run,
        hosts_to_exploit,
        current_depth,
        servers,
        results_callback,
        scan_completed,
        stop,
    ):
        pass


def get_propagation_config(
    default_agent_configuration, scan_target_config: ScanTargetConfiguration
):
    network_scan = NetworkScanConfiguration(
        tcp=default_agent_configuration.propagation.network_scan.tcp,
        icmp=default_agent_configuration.propagation.network_scan.icmp,
        fingerprinters=default_agent_configuration.propagation.network_scan.fingerprinters,
        targets=scan_target_config,
    )
    propagation_config = PropagationConfiguration(
        maximum_depth=default_agent_configuration.propagation.maximum_depth,
        network_scan=network_scan,
        exploitation=default_agent_configuration.propagation.exploitation,
    )
    return propagation_config


class MockExploiter:
    def exploit_hosts(
        self,
        exploiters_to_run,
        hosts_to_exploit,
        current_depth,
        servers,
        results_callback,
        scan_completed,
        stop,
    ):
        scan_completed.wait()
        hte = []
        for _ in range(0, 2):
            hte.append(hosts_to_exploit.get())

        assert hosts_to_exploit.empty()

        for host in hte:
            if host.ip_addr.endswith(".1"):
                results_callback(
                    "PowerShellExploiter",
                    host,
                    ExploiterResultData(True, True, False, os_windows, {}, {}, None),
                )
                results_callback(
                    "SSHExploiter",
                    host,
                    ExploiterResultData(False, False, False, os_linux, {}, {}, "SSH FAILED for .1"),
                )
            elif host.ip_addr.endswith(".2"):
                results_callback(
                    "PowerShellExploiter",
                    host,
                    ExploiterResultData(
                        False, False, False, os_windows, {}, {}, "POWERSHELL FAILED for .2"
                    ),
                )
                results_callback(
                    "SSHExploiter",
                    host,
                    ExploiterResultData(False, False, False, os_linux, {}, {}, "SSH FAILED for .2"),
                )
            elif host.ip_addr.endswith(".3"):
                results_callback(
                    "PowerShellExploiter",
                    host,
                    ExploiterResultData(
                        False, False, False, os_windows, {}, {}, "POWERSHELL FAILED for .3"
                    ),
                )
                results_callback(
                    "SSHExploiter",
                    host,
                    ExploiterResultData(True, True, False, os_linux, {}, {}, None),
                )


def test_scan_target_generation(
    mock_ip_scanner, mock_target_host_factory, default_agent_configuration
):
    local_network_interfaces = [IPv4Interface("10.0.0.9/29")]
    p = Propagator(
        mock_ip_scanner,
        StubExploiter(),
        mock_target_host_factory,
        local_network_interfaces,
    )
    targets = ScanTargetConfiguration(
        blocked_ips=["10.0.0.3"],
        inaccessible_subnets=["10.0.0.128/30", "10.0.0.8/29"],
        scan_my_networks=True,
        subnets=["10.0.0.0/29", "172.10.20.30"],
    )
    propagation_config = get_propagation_config(default_agent_configuration, targets)
    p.propagate(propagation_config, 1, SERVERS, Event())

    expected_ip_scan_list = [
        "10.0.0.0",
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.4",
        "10.0.0.5",
        "10.0.0.6",
        "10.0.0.8",
        "10.0.0.10",
        "10.0.0.11",
        "10.0.0.12",
        "10.0.0.13",
        "10.0.0.14",
        "10.0.0.128",
        "10.0.0.129",
        "10.0.0.130",
        "172.10.20.30",
    ]

    actual_ip_scan_list = [address.ip for address in mock_ip_scanner.scan.call_args_list[0][0][0]]
    assert actual_ip_scan_list == expected_ip_scan_list
