from typing import Dict

from monkeytypes import NetworkPort

from . import AgentConfiguration
from .agent_sub_configurations import (
    ExploitationConfiguration,
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    PolymorphismConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
    TCPScanConfiguration,
)

CREDENTIALS_COLLECTORS: Dict[str, Dict] = {}

PAYLOAD_CONFIGURATION: Dict[str, Dict] = {}

TCP_PORTS: tuple[NetworkPort, ...] = (
    NetworkPort(22),
    NetworkPort(80),
    NetworkPort(135),
    NetworkPort(443),
    NetworkPort(445),
    NetworkPort(2222),
    NetworkPort(3306),
    NetworkPort(3389),
    NetworkPort(5985),
    NetworkPort(5986),
    NetworkPort(7001),
    NetworkPort(8008),
    NetworkPort(8080),
    NetworkPort(8088),
    NetworkPort(8983),
    NetworkPort(9600),
)

TCP_SCAN_CONFIGURATION = TCPScanConfiguration(timeout=3.0, ports=TCP_PORTS)
ICMP_CONFIGURATION = ICMPScanConfiguration(timeout=1.0)

SCAN_TARGET_CONFIGURATION = ScanTargetConfiguration(
    blocked_ips=tuple(), inaccessible_subnets=tuple(), scan_my_networks=False, subnets=tuple()
)
NETWORK_SCAN_CONFIGURATION = NetworkScanConfiguration(
    tcp=TCP_SCAN_CONFIGURATION,
    icmp=ICMP_CONFIGURATION,
    fingerprinters={},
    targets=SCAN_TARGET_CONFIGURATION,
)

EXPLOITATION_CONFIGURATION = ExploitationConfiguration(
    exploiters={},
)

PROPAGATION_CONFIGURATION = PropagationConfiguration(
    maximum_depth=2,
    network_scan=NETWORK_SCAN_CONFIGURATION,
    exploitation=EXPLOITATION_CONFIGURATION,
)

DEFAULT_AGENT_CONFIGURATION = AgentConfiguration(
    keep_tunnel_open_time=30.0,
    credentials_collectors=CREDENTIALS_COLLECTORS,
    payloads=PAYLOAD_CONFIGURATION,
    propagation=PROPAGATION_CONFIGURATION,
    polymorphism=PolymorphismConfiguration(randomize_agent_hash=False),
)
