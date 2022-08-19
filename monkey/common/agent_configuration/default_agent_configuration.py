import dataclasses

from . import AgentConfiguration
from .agent_sub_configurations import (
    CustomPBAConfiguration,
    ExploitationConfiguration,
    ExploitationOptionsConfiguration,
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
    TCPScanConfiguration,
)

PBAS = (
    "CommunicateAsBackdoorUser",
    "ModifyShellStartupFiles",
    "HiddenFiles",
    "TrapCommand",
    "ChangeSetuidSetgid",
    "ScheduleJobs",
    "Timestomping",
    "AccountDiscovery",
    "ProcessListCollection",
)

CREDENTIAL_COLLECTORS = ("MimikatzCollector", "SSHCollector")

PBA_CONFIGURATION = tuple(PluginConfiguration(pba, {}) for pba in PBAS)
CREDENTIAL_COLLECTOR_CONFIGURATION = tuple(
    PluginConfiguration(collector, {}) for collector in CREDENTIAL_COLLECTORS
)

RANSOMWARE_OPTIONS = {
    "encryption": {
        "enabled": True,
        "file_extension": ".m0nk3y",
        "directories": {"linux_target_dir": "", "windows_target_dir": ""},
    },
    "other_behaviors": {"readme": True},
}

PAYLOAD_CONFIGURATION = tuple([PluginConfiguration("ransomware", RANSOMWARE_OPTIONS)])

CUSTOM_PBA_CONFIGURATION = CustomPBAConfiguration(
    linux_command="", linux_filename="", windows_command="", windows_filename=""
)

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
    9200,
    9600,
)

TCP_SCAN_CONFIGURATION = TCPScanConfiguration(timeout=3.0, ports=TCP_PORTS)
ICMP_CONFIGURATION = ICMPScanConfiguration(timeout=1.0)
HTTP_PORTS = (80, 443, 7001, 8008, 8080, 8983, 9200, 9600)
FINGERPRINTERS = (
    PluginConfiguration("elastic", {}),
    # Plugin configuration option contents are not converted to tuples
    PluginConfiguration("http", {"http_ports": list(HTTP_PORTS)}),
    PluginConfiguration("mssql", {}),
    PluginConfiguration("smb", {}),
    PluginConfiguration("ssh", {}),
)

SCAN_TARGET_CONFIGURATION = ScanTargetConfiguration(tuple(), tuple(), True, tuple())
NETWORK_SCAN_CONFIGURATION = NetworkScanConfiguration(
    TCP_SCAN_CONFIGURATION, ICMP_CONFIGURATION, FINGERPRINTERS, SCAN_TARGET_CONFIGURATION
)

EXPLOITATION_OPTIONS_CONFIGURATION = ExploitationOptionsConfiguration(HTTP_PORTS)
BRUTE_FORCE_EXPLOITERS = (
    PluginConfiguration("MSSQLExploiter", {}),
    PluginConfiguration("PowerShellExploiter", {}),
    PluginConfiguration("SSHExploiter", {}),
    PluginConfiguration("SmbExploiter", {"smb_download_timeout": 30}),
    PluginConfiguration("WmiExploiter", {"smb_download_timeout": 30}),
)

VULNERABILITY_EXPLOITERS = (
    PluginConfiguration("Log4ShellExploiter", {}),
    PluginConfiguration("HadoopExploiter", {}),
)

EXPLOITATION_CONFIGURATION = ExploitationConfiguration(
    EXPLOITATION_OPTIONS_CONFIGURATION, BRUTE_FORCE_EXPLOITERS, VULNERABILITY_EXPLOITERS
)

PROPAGATION_CONFIGURATION = PropagationConfiguration(
    maximum_depth=2,
    network_scan=NETWORK_SCAN_CONFIGURATION,
    exploitation=EXPLOITATION_CONFIGURATION,
)

DEFAULT_AGENT_CONFIGURATION = AgentConfiguration(
    keep_tunnel_open_time=30,
    custom_pbas=CUSTOM_PBA_CONFIGURATION,
    post_breach_actions=PBA_CONFIGURATION,
    credential_collectors=CREDENTIAL_COLLECTOR_CONFIGURATION,
    payloads=PAYLOAD_CONFIGURATION,
    propagation=PROPAGATION_CONFIGURATION,
)

DEFAULT_RANSOMWARE_AGENT_CONFIGURATION = dataclasses.replace(
    DEFAULT_AGENT_CONFIGURATION, post_breach_actions=tuple()
)
