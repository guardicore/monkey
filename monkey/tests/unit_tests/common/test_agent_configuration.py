from common import OperatingSystems
from common.configuration import (
    CustomPBAConfigurationSchema,
    ExploitationConfiguration,
    ExploitationConfigurationSchema,
    ExploitationOptionsConfigurationSchema,
    ExploiterConfigurationSchema,
    ICMPScanConfigurationSchema,
    NetworkScanConfiguration,
    NetworkScanConfigurationSchema,
    PluginConfigurationSchema,
    PropagationConfiguration,
    PropagationConfigurationSchema,
    ScanTargetConfigurationSchema,
    TCPScanConfigurationSchema,
)


def test_build_plugin_configuration():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
    schema = PluginConfigurationSchema()

    config = schema.load({"name": name, "options": options})

    assert config.name == name
    assert config.options == options


def test_custom_pba_configuration_schema():
    linux_command = "a"
    linux_filename = "b"
    windows_command = "c"
    windows_filename = "d"
    schema = CustomPBAConfigurationSchema()

    config = schema.load(
        {
            "linux_command": linux_command,
            "linux_filename": linux_filename,
            "windows_command": windows_command,
            "windows_filename": windows_filename,
        }
    )

    assert config.linux_command == linux_command
    assert config.linux_filename == linux_filename
    assert config.windows_command == windows_command
    assert config.windows_filename == windows_filename


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


TIMEOUT_MS = 2525
ICMP_CONFIGURATION = {"timeout_ms": TIMEOUT_MS}


def test_icmp_scan_configuration_schema():
    schema = ICMPScanConfigurationSchema()

    config = schema.load(ICMP_CONFIGURATION)

    assert config.timeout_ms == TIMEOUT_MS


TIMEOUT_MS = 2525
PORTS = [8080, 443]

TCP_SCAN_CONFIGURATION = {"timeout_ms": TIMEOUT_MS, "ports": PORTS}


def test_tcp_scan_configuration_schema():
    schema = TCPScanConfigurationSchema()

    config = schema.load(TCP_SCAN_CONFIGURATION)

    assert config.timeout_ms == TIMEOUT_MS
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
    assert config.tcp.timeout_ms == TCP_SCAN_CONFIGURATION["timeout_ms"]
    assert config.icmp.timeout_ms == ICMP_CONFIGURATION["timeout_ms"]
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

    assert config_dict == PROPAGATION_CONFIGURATION
