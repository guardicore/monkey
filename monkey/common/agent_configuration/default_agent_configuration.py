from copy import deepcopy
from typing import Dict

from . import AgentConfiguration
from .agent_sub_configurations import (
    ExploitationConfiguration,
    ExploitationOptionsConfiguration,
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
    TCPScanConfiguration,
)

CREDENTIALS_COLLECTORS: Dict[str, Dict] = {"MimikatzCollector": {}, "SSHCollector": {}}

RANSOMWARE_OPTIONS = {
    "encryption": {
        "enabled": True,
        "file_extension": ".m0nk3y",
        "directories": {"linux_target_dir": "", "windows_target_dir": ""},
    },
    "other_behaviors": {"readme": True},
}

PAYLOAD_CONFIGURATION = {"ransomware": RANSOMWARE_OPTIONS}

TCP_PORTS = (
    22,
    80,
    135,
    443,
    445,
    2222,
    3306,
    3389,
    5985,
    5986,
    7001,
    8008,
    8080,
    8088,
    8983,
    9600,
)

TCP_SCAN_CONFIGURATION = TCPScanConfiguration(timeout=3.0, ports=TCP_PORTS)
ICMP_CONFIGURATION = ICMPScanConfiguration(timeout=1.0)
HTTP_PORTS = (80, 443, 7001, 8008, 8080, 8983, 9600)
FINGERPRINTERS = (
    # Plugin configuration option contents are not converted to tuples
    PluginConfiguration(name="http", options={"http_ports": list(HTTP_PORTS)}),
    PluginConfiguration(name="mssql", options={}),
    PluginConfiguration(name="smb", options={}),
    PluginConfiguration(name="ssh", options={}),
)

SCAN_TARGET_CONFIGURATION = ScanTargetConfiguration(
    blocked_ips=tuple(), inaccessible_subnets=tuple(), scan_my_networks=False, subnets=tuple()
)
NETWORK_SCAN_CONFIGURATION = NetworkScanConfiguration(
    tcp=TCP_SCAN_CONFIGURATION,
    icmp=ICMP_CONFIGURATION,
    fingerprinters=FINGERPRINTERS,
    targets=SCAN_TARGET_CONFIGURATION,
)

EXPLOITATION_OPTIONS_CONFIGURATION = ExploitationOptionsConfiguration(http_ports=HTTP_PORTS)

# Order is preserved and agent will run exploiters in this sequence
EXPLOITERS: Dict[str, Dict] = {
    "Log4ShellExploiter": {},
    "MSSQLExploiter": {},
    "PowerShellExploiter": {},
    "SSHExploiter": {},
}

EXPLOITATION_CONFIGURATION = ExploitationConfiguration(
    options=EXPLOITATION_OPTIONS_CONFIGURATION,
    exploiters=EXPLOITERS,
)

PROPAGATION_CONFIGURATION = PropagationConfiguration(
    maximum_depth=2,
    network_scan=NETWORK_SCAN_CONFIGURATION,
    exploitation=EXPLOITATION_CONFIGURATION,
)

DEFAULT_AGENT_CONFIGURATION = AgentConfiguration(
    keep_tunnel_open_time=30,
    credentials_collectors=CREDENTIALS_COLLECTORS,
    payloads=PAYLOAD_CONFIGURATION,
    propagation=PROPAGATION_CONFIGURATION,
)

DEFAULT_RANSOMWARE_AGENT_CONFIGURATION = deepcopy(DEFAULT_AGENT_CONFIGURATION)
DEFAULT_RANSOMWARE_AGENT_CONFIGURATION.credentials_collectors = {}
