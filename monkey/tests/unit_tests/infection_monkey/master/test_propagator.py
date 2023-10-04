from ipaddress import IPv4Address, IPv4Interface
from threading import Event
from unittest.mock import MagicMock

import pytest
from monkeytypes import OperatingSystem

from common.agent_configuration.agent_sub_configurations import (
    NetworkScanConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
)
from common.types import DiscoveredService, NetworkProtocol, NetworkService, PortStatus
from infection_monkey.i_puppet import FingerprintData, PingScanData, PortScanData, TargetHost
from infection_monkey.master import Exploiter, IPScanResults, Propagator

empty_fingerprint_data = FingerprintData(os_type=None, os_version=None, services=[])

dot_1_scan_results = IPScanResults(
    PingScanData(response_received=True, os=OperatingSystem.WINDOWS),
    {
        22: PortScanData(port=22, status=PortStatus.CLOSED),
        445: PortScanData(
            port=445, status=PortStatus.OPEN, banner="SMB BANNER", service=NetworkService.SMB
        ),
        3389: PortScanData(
            port=3389, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN
        ),
    },
    {
        "SMBFinger": FingerprintData(
            os_type=OperatingSystem.WINDOWS,
            os_version="vista",
            services=[
                DiscoveredService(
                    protocol=NetworkProtocol.TCP, port=445, service=NetworkService.SMB
                )
            ],
        ),
        "SSHFinger": empty_fingerprint_data,
        "HTTPFinger": empty_fingerprint_data,
    },
)

dot_2_scan_results = IPScanResults(
    PingScanData(response_received=True, os=OperatingSystem.LINUX),
    {
        99: PortScanData(
            port=99, status=PortStatus.OPEN, banner="", service=NetworkService.UNKNOWN
        ),
    },
    {
        "FirstFinger": FingerprintData(
            os_type=OperatingSystem.WINDOWS,
            os_version="7",
            services=[
                DiscoveredService(
                    protocol=NetworkProtocol.UDP, port=99, service=NetworkService.MSSQL
                )
            ],
        ),
        "99Finger": FingerprintData(
            os_type=OperatingSystem.WINDOWS,
            os_version="7",
            services=[
                DiscoveredService(
                    protocol=NetworkProtocol.UDP, port=99, service=NetworkService.UNKNOWN
                )
            ],
        ),
    },
)

dot_3_scan_results = IPScanResults(
    PingScanData(response_received=True, os=OperatingSystem.LINUX),
    {
        22: PortScanData(
            port=22, status=PortStatus.OPEN, banner="SSH BANNER", service=NetworkService.SSH
        ),
        443: PortScanData(
            port=443, status=PortStatus.OPEN, banner="HTTPS BANNER", service=NetworkService.HTTPS
        ),
        3389: PortScanData(port=3389, status=PortStatus.CLOSED, banner=""),
    },
    {
        "SSHFinger": FingerprintData(
            os_type=OperatingSystem.LINUX,
            os_version="ubuntu",
            services=[
                DiscoveredService(protocol=NetworkProtocol.TCP, port=22, service=NetworkService.SSH)
            ],
        ),
        "HTTPFinger": FingerprintData(
            os_type=None,
            os_version=None,
            services=[
                DiscoveredService(
                    protocol=NetworkProtocol.TCP, port=80, service=NetworkService.HTTP
                ),
                DiscoveredService(
                    protocol=NetworkProtocol.TCP, port=443, service=NetworkService.HTTPS
                ),
            ],
        ),
        "SMBFinger": empty_fingerprint_data,
    },
)

dead_host_scan_results = IPScanResults(
    PingScanData(response_received=False, os=None),
    {
        22: PortScanData(port=22, status=PortStatus.CLOSED),
        443: PortScanData(port=443, status=PortStatus.CLOSED),
        3389: PortScanData(port=3389, status=PortStatus.CLOSED, banner=""),
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
            elif address.ip.endswith(".2"):
                results_callback(address, dot_2_scan_results)
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


def test_scan_target_generation(mock_ip_scanner, default_agent_configuration):
    local_network_interfaces = [IPv4Interface("10.0.0.9/29")]
    p = Propagator(
        mock_ip_scanner,
        StubExploiter(),
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


def scan_host(ip: str, ip_scanner, default_agent_configuration) -> TargetHost:
    mock_exploiter = MagicMock(spec=Exploiter)
    p = Propagator(
        ip_scanner,
        mock_exploiter,
        [],
    )
    targets = ScanTargetConfiguration(subnets=[ip])
    propagation_config = get_propagation_config(default_agent_configuration, targets)
    p.propagate(propagation_config, 1, SERVERS, Event())

    args, _ = mock_exploiter.exploit_hosts.call_args
    hosts = args[1]
    return hosts.get(block=False)


#
def test_targethost_updated_from_pingscan(mock_ip_scanner, default_agent_configuration):
    host = scan_host("10.0.0.1", mock_ip_scanner, default_agent_configuration)

    assert host.ip == IPv4Address("10.0.0.1")
    assert host.icmp is True
    assert host.operating_system == OperatingSystem.WINDOWS


def test_targethost_updated_from_fingerprinters(mock_ip_scanner, default_agent_configuration):
    host = scan_host("10.0.0.1", mock_ip_scanner, default_agent_configuration)

    assert host.ports_status.tcp_ports[445].protocol == NetworkProtocol.TCP
    assert host.ports_status.tcp_ports[445].service == NetworkService.SMB


def test_targethost_udpated_from_portscan(mock_ip_scanner, default_agent_configuration):
    host = scan_host("10.0.0.3", mock_ip_scanner, default_agent_configuration)

    # port, status, banner
    # protocol, service
    assert host.ports_status.tcp_ports[22].port == 22
    assert host.ports_status.tcp_ports[22].status == PortStatus.OPEN
    assert host.ports_status.tcp_ports[22].banner == "SSH BANNER"
    assert host.ports_status.tcp_ports[443].port == 443
    assert host.ports_status.tcp_ports[443].status == PortStatus.OPEN
    assert host.ports_status.tcp_ports[443].banner == "HTTPS BANNER"
    assert host.ports_status.tcp_ports[3389].port == 3389
    assert host.ports_status.tcp_ports[3389].status == PortStatus.CLOSED
    assert host.ports_status.tcp_ports[3389].banner == ""


def test_targethost_protocol_unknown_without_fingerprinter(
    mock_ip_scanner, default_agent_configuration
):
    host = scan_host("10.0.0.3", mock_ip_scanner, default_agent_configuration)

    assert host.ports_status.tcp_ports[3389].protocol == NetworkProtocol.UNKNOWN


def test_targethost_fingerprinter_updates_os(mock_ip_scanner, default_agent_configuration):
    host = scan_host("10.0.0.2", mock_ip_scanner, default_agent_configuration)

    assert host.operating_system == OperatingSystem.WINDOWS


def test_targethost_doesnt_replace_service_with_unknown(
    mock_ip_scanner, default_agent_configuration
):
    host = scan_host("10.0.0.2", mock_ip_scanner, default_agent_configuration)

    assert host.ports_status.udp_ports[99].service == NetworkService.MSSQL


def test_targethost_fingerprint_applies_to_correct_protocol(
    mock_ip_scanner, default_agent_configuration
):
    host = scan_host("10.0.0.2", mock_ip_scanner, default_agent_configuration)

    assert len(host.ports_status.tcp_ports) == 1
    assert len(host.ports_status.udp_ports) == 1
    assert host.ports_status.tcp_ports[99].service == NetworkService.UNKNOWN
