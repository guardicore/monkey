from typing import Tuple

from common.agent_configuration import (
    AgentConfiguration,
    ExploitationConfiguration,
    ExploitationOptionsConfiguration,
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
    TCPScanConfiguration,
)
from common.credentials import Credentials

from . import TestConfiguration

_tcp_scan_configuration = TCPScanConfiguration(timeout=3.0, ports=[])
_icmp_scan_configuration = ICMPScanConfiguration(timeout=1.0)
_scan_target_configuration = ScanTargetConfiguration(
    blocked_ips=[], inaccessible_subnets=[], scan_my_networks=False, subnets=[]
)
_network_scan_configuration = NetworkScanConfiguration(
    tcp=_tcp_scan_configuration,
    icmp=_icmp_scan_configuration,
    fingerprinters=[],
    targets=_scan_target_configuration,
)

_exploitation_options_configuration = ExploitationOptionsConfiguration(http_ports=[])
_exploitation_configuration = ExploitationConfiguration(
    options=_exploitation_options_configuration, exploiters=[]
)

_propagation_configuration = PropagationConfiguration(
    maximum_depth=0,
    network_scan=_network_scan_configuration,
    exploitation=_exploitation_configuration,
)

_agent_configuration = AgentConfiguration(
    keep_tunnel_open_time=0,
    credentials_collectors={},
    payloads={},
    propagation=_propagation_configuration,
)
_propagation_credentials: Tuple[Credentials, ...] = tuple()

# This is an empty, NOOP configuration from which other configurations can be built
noop_test_configuration: TestConfiguration = TestConfiguration(
    agent_configuration=_agent_configuration, propagation_credentials=_propagation_credentials
)
