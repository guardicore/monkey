import json

from tests.common.example_agent_configuration import (
    AGENT_CONFIGURATION,
    BLOCKED_IPS,
    CUSTOM_PBA_CONFIGURATION,
    EXPLOITATION_CONFIGURATION,
    FINGERPRINTERS,
    ICMP_CONFIGURATION,
    INACCESSIBLE_SUBNETS,
    LINUX_COMMAND,
    LINUX_FILENAME,
    LOCAL_NETWORK_SCAN,
    NETWORK_SCAN_CONFIGURATION,
    PLUGIN_CONFIGURATION,
    PLUGIN_NAME,
    PLUGIN_OPTIONS,
    PORTS,
    PROPAGATION_CONFIGURATION,
    SCAN_TARGET_CONFIGURATION,
    SUBNETS,
    TCP_SCAN_CONFIGURATION,
    TIMEOUT,
    WINDOWS_COMMAND,
    WINDOWS_FILENAME,
)

from common.configuration import (
    DEFAULT_AGENT_CONFIGURATION_JSON,
    AgentConfiguration,
    AgentConfigurationSchema,
)
from common.configuration.agent_sub_configuration_schemas import (
    CustomPBAConfigurationSchema,
    ExploitationConfigurationSchema,
    ExploitationOptionsConfigurationSchema,
    ExploiterConfigurationSchema,
    ICMPScanConfigurationSchema,
    NetworkScanConfigurationSchema,
    PluginConfigurationSchema,
    PropagationConfigurationSchema,
    ScanTargetConfigurationSchema,
    TCPScanConfigurationSchema,
)
from common.configuration.agent_sub_configurations import (
    CustomPBAConfiguration,
    ExploitationConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
)


def test_build_plugin_configuration():
    schema = PluginConfigurationSchema()

    config = schema.load(PLUGIN_CONFIGURATION)

    assert config.name == PLUGIN_NAME
    assert config.options == PLUGIN_OPTIONS


def test_custom_pba_configuration_schema():
    schema = CustomPBAConfigurationSchema()

    config = schema.load(CUSTOM_PBA_CONFIGURATION)

    assert config.linux_command == LINUX_COMMAND
    assert config.linux_filename == LINUX_FILENAME
    assert config.windows_command == WINDOWS_COMMAND
    assert config.windows_filename == WINDOWS_FILENAME


def test_scan_target_configuration():
    schema = ScanTargetConfigurationSchema()

    config = schema.load(SCAN_TARGET_CONFIGURATION)

    assert config.blocked_ips == BLOCKED_IPS
    assert config.inaccessible_subnets == INACCESSIBLE_SUBNETS
    assert config.local_network_scan == LOCAL_NETWORK_SCAN
    assert config.subnets == SUBNETS


def test_icmp_scan_configuration_schema():
    schema = ICMPScanConfigurationSchema()

    config = schema.load(ICMP_CONFIGURATION)

    assert config.timeout == TIMEOUT


def test_tcp_scan_configuration_schema():
    schema = TCPScanConfigurationSchema()

    config = schema.load(TCP_SCAN_CONFIGURATION)

    assert config.timeout == TIMEOUT
    assert config.ports == PORTS


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
    schema = ExploiterConfigurationSchema()

    config = schema.load({"name": name, "options": options})

    assert config.name == name
    assert config.options == options


def test_exploitation_configuration():
    schema = ExploitationConfigurationSchema()

    config = schema.load(EXPLOITATION_CONFIGURATION)
    config_dict = schema.dump(config)

    assert isinstance(config, ExploitationConfiguration)
    assert config_dict == EXPLOITATION_CONFIGURATION


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
    schema = AgentConfigurationSchema()

    config = schema.load(AGENT_CONFIGURATION)
    config_dict = schema.dump(config)

    assert isinstance(config, AgentConfiguration)
    assert config.keep_tunnel_open_time == 30
    assert isinstance(config.custom_pbas, CustomPBAConfiguration)
    assert isinstance(config.post_breach_actions[0], PluginConfiguration)
    assert isinstance(config.credential_collectors[0], PluginConfiguration)
    assert isinstance(config.payloads[0], PluginConfiguration)
    assert isinstance(config.propagation, PropagationConfiguration)
    assert config_dict == AGENT_CONFIGURATION


def test_default_agent_configuration():
    schema = AgentConfigurationSchema()

    config = schema.loads(DEFAULT_AGENT_CONFIGURATION_JSON)

    assert isinstance(config, AgentConfiguration)


def test_from_dict():
    schema = AgentConfigurationSchema()
    dict_ = json.loads(DEFAULT_AGENT_CONFIGURATION_JSON)

    config = AgentConfiguration.from_dict(dict_)

    assert schema.dump(config) == dict_
