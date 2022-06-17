from common import OperatingSystems
from common.configuration import (
    AgentConfiguration,
    AgentConfigurationSchema,
    CustomPBAConfiguration,
    CustomPBAConfigurationSchema,
    ExploitationConfiguration,
    ExploitationConfigurationSchema,
    ExploitationOptionsConfigurationSchema,
    ExploiterConfigurationSchema,
    ICMPScanConfigurationSchema,
    NetworkScanConfiguration,
    NetworkScanConfigurationSchema,
    PluginConfiguration,
    PluginConfigurationSchema,
    PropagationConfiguration,
    PropagationConfigurationSchema,
    ScanTargetConfigurationSchema,
    TCPScanConfigurationSchema,
)

NAME = "bond"
OPTIONS = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
PLUGIN_CONFIGURATION = {"name": NAME, "options": OPTIONS}


def test_build_plugin_configuration():
    schema = PluginConfigurationSchema()

    config = schema.load(PLUGIN_CONFIGURATION)

    assert config.name == NAME
    assert config.options == OPTIONS


LINUX_COMMAND = "a"
LINUX_FILENAME = "b"
WINDOWS_COMMAND = "c"
WINDOWS_FILENAME = "d"
CUSTOM_PBA_CONFIGURATION = {
    "linux_command": LINUX_COMMAND,
    "linux_filename": LINUX_FILENAME,
    "windows_command": WINDOWS_COMMAND,
    "windows_filename": WINDOWS_FILENAME,
}


def test_custom_pba_configuration_schema():
    schema = CustomPBAConfigurationSchema()

    config = schema.load(CUSTOM_PBA_CONFIGURATION)

    assert config.linux_command == LINUX_COMMAND
    assert config.linux_filename == LINUX_FILENAME
    assert config.windows_command == WINDOWS_COMMAND
    assert config.windows_filename == WINDOWS_FILENAME


BLOCKED_IPS = ["10.0.0.1", "192.168.1.1"]
INACCESSIBLE_SUBNETS = ["172.0.0.0/24", "172.2.2.0/24", "192.168.56.0/24"]
LOCAL_NETWORK_SCAN = True
SUBNETS = ["10.0.0.2", "10.0.0.2/16"]
SCAN_TARGET_CONFIGURATION = {
    "blocked_ips": BLOCKED_IPS,
    "inaccessible_subnets": INACCESSIBLE_SUBNETS,
    "local_network_scan": LOCAL_NETWORK_SCAN,
    "subnets": SUBNETS,
}


def test_scan_target_configuration():
    schema = ScanTargetConfigurationSchema()

    config = schema.load(SCAN_TARGET_CONFIGURATION)

    assert config.blocked_ips == BLOCKED_IPS
    assert config.inaccessible_subnets == INACCESSIBLE_SUBNETS
    assert config.local_network_scan == LOCAL_NETWORK_SCAN
    assert config.subnets == SUBNETS


TIMEOUT = 2.525
ICMP_CONFIGURATION = {"timeout": TIMEOUT}


def test_icmp_scan_configuration_schema():
    schema = ICMPScanConfigurationSchema()

    config = schema.load(ICMP_CONFIGURATION)

    assert config.timeout == TIMEOUT


PORTS = [8080, 443]

TCP_SCAN_CONFIGURATION = {"timeout": TIMEOUT, "ports": PORTS}


def test_tcp_scan_configuration_schema():
    schema = TCPScanConfigurationSchema()

    config = schema.load(TCP_SCAN_CONFIGURATION)

    assert config.timeout == TIMEOUT
    assert config.ports == PORTS


FINGERPRINTERS = [{"name": "mssql", "options": {}}]
NETWORK_SCAN_CONFIGURATION = {
    "tcp": TCP_SCAN_CONFIGURATION,
    "icmp": ICMP_CONFIGURATION,
    "fingerprinters": FINGERPRINTERS,
    "targets": SCAN_TARGET_CONFIGURATION,
}


def test_network_scan_configuration():
    schema = NetworkScanConfigurationSchema()

    config = schema.load(NETWORK_SCAN_CONFIGURATION)

    assert config.tcp.ports == TCP_SCAN_CONFIGURATION["ports"]
    assert config.tcp.timeout == TCP_SCAN_CONFIGURATION["timeout"]
    assert config.icmp.timeout == ICMP_CONFIGURATION["timeout"]
    assert config.fingerprinters[0].name == FINGERPRINTERS[0]["name"]
    assert config.fingerprinters[0].options == FINGERPRINTERS[0]["options"]
    assert config.targets.blocked_ips == BLOCKED_IPS
    assert config.targets.inaccessible_subnets == INACCESSIBLE_SUBNETS
    assert config.targets.local_network_scan == LOCAL_NETWORK_SCAN
    assert config.targets.subnets == SUBNETS


def test_exploitation_options_configuration_schema():
    ports = [1, 2, 3]
    schema = ExploitationOptionsConfigurationSchema()

    config = schema.load({"http_ports": ports})

    assert config.http_ports == ports


def test_exploiter_configuration_schema():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
    supported_os = [OperatingSystems.LINUX, OperatingSystems.WINDOWS]
    schema = ExploiterConfigurationSchema()

    config = schema.load(
        {"name": name, "options": options, "supported_os": [os_.name for os_ in supported_os]}
    )

    assert config.name == name
    assert config.options == options
    assert config.supported_os == supported_os


BRUTE_FORCE = [
    {"name": "ex1", "options": {}, "supported_os": ["LINUX"]},
    {
        "name": "ex2",
        "options": {"smb_download_timeout": 10},
        "supported_os": ["LINUX", "WINDOWS"],
    },
]
VULNERABILITY = [
    {
        "name": "ex3",
        "options": {"smb_download_timeout": 10},
        "supported_os": ["WINDOWS"],
    },
]
EXPLOITATION_CONFIGURATION = {
    "options": {"http_ports": PORTS},
    "brute_force": BRUTE_FORCE,
    "vulnerability": VULNERABILITY,
}


def test_exploitation_configuration():
    schema = ExploitationConfigurationSchema()

    config = schema.load(EXPLOITATION_CONFIGURATION)
    config_dict = schema.dump(config)

    assert isinstance(config, ExploitationConfiguration)
    assert config_dict == EXPLOITATION_CONFIGURATION


PROPAGATION_CONFIGURATION = {
    "maximum_depth": 5,
    "network_scan": NETWORK_SCAN_CONFIGURATION,
    "exploitation": EXPLOITATION_CONFIGURATION,
}


def test_propagation_configuration():
    schema = PropagationConfigurationSchema()

    config = schema.load(PROPAGATION_CONFIGURATION)
    config_dict = schema.dump(config)

    assert isinstance(config, PropagationConfiguration)
    assert isinstance(config.network_scan, NetworkScanConfiguration)
    assert isinstance(config.exploitation, ExploitationConfiguration)
    assert config.maximum_depth == 5
    assert config_dict == PROPAGATION_CONFIGURATION


def test_agent_configuration():
    agent_configuration = {
        "keep_tunnel_open_time": 30,
        "custom_pbas": CUSTOM_PBA_CONFIGURATION,
        "post_breach_actions": [PLUGIN_CONFIGURATION],
        "credential_collectors": [PLUGIN_CONFIGURATION],
        "payloads": [PLUGIN_CONFIGURATION],
        "propagation": PROPAGATION_CONFIGURATION,
    }
    schema = AgentConfigurationSchema()

    config = schema.load(agent_configuration)
    config_dict = schema.dump(config)

    assert isinstance(config, AgentConfiguration)
    assert config.keep_tunnel_open_time == 30
    assert isinstance(config.custom_pbas, CustomPBAConfiguration)
    assert isinstance(config.post_breach_actions[0], PluginConfiguration)
    assert isinstance(config.credential_collectors[0], PluginConfiguration)
    assert isinstance(config.payloads[0], PluginConfiguration)
    assert isinstance(config.propagation, PropagationConfiguration)
    assert config_dict == agent_configuration
