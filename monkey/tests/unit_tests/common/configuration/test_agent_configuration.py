import json
from copy import deepcopy

import pytest
from marshmallow import ValidationError
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

from common.agent_configuration import AgentConfiguration, InvalidConfigurationError
from common.agent_configuration.agent_sub_configuration_schemas import (
    CustomPBAConfigurationSchema,
    ExploitationConfigurationSchema,
    ExploitationOptionsConfigurationSchema,
    ICMPScanConfigurationSchema,
    NetworkScanConfigurationSchema,
    PluginConfigurationSchema,
    PropagationConfigurationSchema,
    ScanTargetConfigurationSchema,
    TCPScanConfigurationSchema,
)
from common.agent_configuration.agent_sub_configurations import (
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


def test_custom_pba_configuration_schema__empty_filename_allowed():
    schema = CustomPBAConfigurationSchema()

    empty_filename_configuration = CUSTOM_PBA_CONFIGURATION.copy()
    empty_filename_configuration.update({"linux_filename": ""})

    config = schema.load(empty_filename_configuration)

    assert config.linux_command == LINUX_COMMAND
    assert config.linux_filename == ""
    assert config.windows_command == WINDOWS_COMMAND
    assert config.windows_filename == WINDOWS_FILENAME


def test_custom_pba_configuration_schema__invalid_filename():
    schema = CustomPBAConfigurationSchema()

    invalid_filename_configuration = CUSTOM_PBA_CONFIGURATION.copy()
    invalid_filename_configuration["linux_filename"] = "???"

    with pytest.raises(ValidationError):
        schema.load(invalid_filename_configuration)


def test_scan_target_configuration():
    schema = ScanTargetConfigurationSchema()

    config = schema.load(SCAN_TARGET_CONFIGURATION)

    assert config.blocked_ips == tuple(BLOCKED_IPS)
    assert config.inaccessible_subnets == tuple(INACCESSIBLE_SUBNETS)
    assert config.local_network_scan == LOCAL_NETWORK_SCAN
    assert config.subnets == tuple(SUBNETS)


def test_icmp_scan_configuration_schema():
    schema = ICMPScanConfigurationSchema()

    config = schema.load(ICMP_CONFIGURATION)

    assert config.timeout == TIMEOUT


def test_tcp_scan_configuration_schema():
    schema = TCPScanConfigurationSchema()

    config = schema.load(TCP_SCAN_CONFIGURATION)

    assert config.timeout == TIMEOUT
    assert config.ports == tuple(PORTS)


def test_network_scan_configuration():
    schema = NetworkScanConfigurationSchema()

    config = schema.load(NETWORK_SCAN_CONFIGURATION)

    assert config.tcp.ports == tuple(TCP_SCAN_CONFIGURATION["ports"])
    assert config.tcp.timeout == TCP_SCAN_CONFIGURATION["timeout"]
    assert config.icmp.timeout == ICMP_CONFIGURATION["timeout"]
    assert config.fingerprinters[0].name == FINGERPRINTERS[0]["name"]
    assert config.fingerprinters[0].options == FINGERPRINTERS[0]["options"]
    assert config.targets.blocked_ips == tuple(BLOCKED_IPS)
    assert config.targets.inaccessible_subnets == tuple(INACCESSIBLE_SUBNETS)
    assert config.targets.local_network_scan == LOCAL_NETWORK_SCAN
    assert config.targets.subnets == tuple(SUBNETS)


def test_exploitation_options_configuration_schema():
    ports = [1, 2, 3]
    schema = ExploitationOptionsConfigurationSchema()

    config = schema.load({"http_ports": ports})

    assert config.http_ports == tuple(ports)


def test_exploiter_configuration_schema():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
    schema = PluginConfigurationSchema()

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
    config = AgentConfiguration.from_mapping(AGENT_CONFIGURATION)
    config_json = AgentConfiguration.to_json(config)

    assert isinstance(config, AgentConfiguration)
    assert config.keep_tunnel_open_time == 30
    assert isinstance(config.custom_pbas, CustomPBAConfiguration)
    assert isinstance(config.post_breach_actions[0], PluginConfiguration)
    assert isinstance(config.credential_collectors[0], PluginConfiguration)
    assert isinstance(config.payloads[0], PluginConfiguration)
    assert isinstance(config.propagation, PropagationConfiguration)
    assert json.loads(config_json) == AGENT_CONFIGURATION


def test_incorrect_type():
    valid_config = AgentConfiguration.from_mapping(AGENT_CONFIGURATION)
    with pytest.raises(InvalidConfigurationError):
        valid_config_dict = valid_config.__dict__
        valid_config_dict["keep_tunnel_open_time"] = "not_a_float"
        AgentConfiguration(**valid_config_dict)


def test_to_from_mapping():
    config = AgentConfiguration.from_mapping(AGENT_CONFIGURATION)

    assert AgentConfiguration.to_mapping(config) == AGENT_CONFIGURATION


def test_from_mapping__invalid_data():
    dict_ = deepcopy(AGENT_CONFIGURATION)
    dict_["payloads"] = "payloads"

    with pytest.raises(InvalidConfigurationError):
        AgentConfiguration.from_mapping(dict_)


def test_to_from_json():
    original_config = AgentConfiguration.from_mapping(AGENT_CONFIGURATION)
    config_json = AgentConfiguration.to_json(original_config)

    assert AgentConfiguration.from_json(config_json) == original_config


def test_from_json__invalid_data():
    invalid_dict = deepcopy(AGENT_CONFIGURATION)
    invalid_dict["payloads"] = "payloads"

    with pytest.raises(InvalidConfigurationError):
        AgentConfiguration.from_json(json.dumps(invalid_dict))
