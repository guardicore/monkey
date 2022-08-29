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

PBA_CONFIGURATION = tuple(PluginConfiguration(name=pba, options={}) for pba in PBAS)
CREDENTIAL_COLLECTOR_CONFIGURATION = tuple(
    PluginConfiguration(name=collector, options={}) for collector in CREDENTIAL_COLLECTORS
)

RANSOMWARE_OPTIONS = {
    "encryption": {
        "enabled": True,
        "file_extension": ".m0nk3y",
        "directories": {"linux_target_dir": "", "windows_target_dir": ""},
    },
    "other_behaviors": {"readme": True},
}

PAYLOAD_CONFIGURATION = tuple([PluginConfiguration(name="ransomware", options=RANSOMWARE_OPTIONS)])

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
    PluginConfiguration(name="elastic", options={}),
    # Plugin configuration option contents are not converted to tuples
    PluginConfiguration(name="http", options={"http_ports": list(HTTP_PORTS)}),
    PluginConfiguration(name="mssql", options={}),
    PluginConfiguration(name="smb", options={}),
    PluginConfiguration(name="ssh", options={}),
)

SCAN_TARGET_CONFIGURATION = ScanTargetConfiguration(
    blocked_ips=tuple(), inaccessible_subnets=tuple(), local_network_scan=True, subnets=tuple()
)
NETWORK_SCAN_CONFIGURATION = NetworkScanConfiguration(
    tcp=TCP_SCAN_CONFIGURATION,
    icmp=ICMP_CONFIGURATION,
    fingerprinters=FINGERPRINTERS,
    targets=SCAN_TARGET_CONFIGURATION,
)

EXPLOITATION_OPTIONS_CONFIGURATION = ExploitationOptionsConfiguration(http_ports=HTTP_PORTS)
BRUTE_FORCE_EXPLOITERS = (
    PluginConfiguration(name="MSSQLExploiter", options={}),
    PluginConfiguration(name="PowerShellExploiter", options={}),
    PluginConfiguration(name="SSHExploiter", options={}),
    PluginConfiguration(name="SmbExploiter", options={"smb_download_timeout": 30}),
    PluginConfiguration(name="WmiExploiter", options={"smb_download_timeout": 30}),
)

VULNERABILITY_EXPLOITERS = (
    PluginConfiguration(name="Log4ShellExploiter", options={}),
    PluginConfiguration(name="HadoopExploiter", options={}),
)

EXPLOITATION_CONFIGURATION = ExploitationConfiguration(
    options=EXPLOITATION_OPTIONS_CONFIGURATION,
    brute_force=BRUTE_FORCE_EXPLOITERS,
    vulnerability=VULNERABILITY_EXPLOITERS,
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

DEFAULT_RANSOMWARE_AGENT_CONFIGURATION = DEFAULT_AGENT_CONFIGURATION.copy(
    update={"post_breach_actions": tuple()}
)
