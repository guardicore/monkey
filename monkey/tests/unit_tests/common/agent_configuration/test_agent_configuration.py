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

from common.agent_configuration import InvalidConfigurationError
from common.agent_configuration.agent_configuration import Pydantic___AgentConfiguration
from common.agent_configuration.agent_sub_configurations import (
    Pydantic___CustomPBAConfiguration,
    Pydantic___ExploitationConfiguration,
    Pydantic___ExploitationOptionsConfiguration,
    Pydantic___ICMPScanConfiguration,
    Pydantic___NetworkScanConfiguration,
    Pydantic___PluginConfiguration,
    Pydantic___PropagationConfiguration,
    Pydantic___ScanTargetConfiguration,
    Pydantic___TCPScanConfiguration,
)

INVALID_PORTS = [[-1, 1, 2], [1, 2, 99999]]


def test_build_plugin_configuration():
    config = Pydantic___PluginConfiguration(**PLUGIN_CONFIGURATION)

    assert config.name == PLUGIN_NAME
    assert config.options == PLUGIN_OPTIONS


def test_custom_pba_configuration_schema():
    config = Pydantic___CustomPBAConfiguration(**CUSTOM_PBA_CONFIGURATION)

    assert config.linux_command == LINUX_COMMAND
    assert config.linux_filename == LINUX_FILENAME
    assert config.windows_command == WINDOWS_COMMAND
    assert config.windows_filename == WINDOWS_FILENAME


def test_custom_pba_configuration_schema__empty_filenames_allowed():
    empty_filename_configuration = CUSTOM_PBA_CONFIGURATION.copy()
    empty_filename_configuration.update({"linux_filename": "", "windows_filename": ""})

    config = Pydantic___CustomPBAConfiguration(**empty_filename_configuration)

    assert config.linux_command == LINUX_COMMAND
    assert config.linux_filename == ""
    assert config.windows_command == WINDOWS_COMMAND
    assert config.windows_filename == ""


@pytest.mark.parametrize("linux_filename", ["/", "/abc/", "\0"])
def test_custom_pba_configuration_schema__invalid_linux_filename(linux_filename):
    invalid_filename_configuration = CUSTOM_PBA_CONFIGURATION.copy()
    invalid_filename_configuration["linux_filename"] = linux_filename

    with pytest.raises(ValidationError):
        Pydantic___CustomPBAConfiguration(**invalid_filename_configuration)


@pytest.mark.parametrize(
    "windows_filename", ["CON", "CON.txt", "con.abc.pdf", " ", "abc.", "a?b", "d\\e"]
)
def test_custom_pba_configuration_schema__invalid_windows_filename(windows_filename):
    invalid_filename_configuration = CUSTOM_PBA_CONFIGURATION.copy()
    invalid_filename_configuration["windows_filename"] = windows_filename

    with pytest.raises(ValidationError):
        Pydantic___CustomPBAConfiguration(**invalid_filename_configuration)


def test_scan_target_configuration():
    config = Pydantic___ScanTargetConfiguration(**SCAN_TARGET_CONFIGURATION)

    assert config.blocked_ips == tuple(BLOCKED_IPS)
    assert config.inaccessible_subnets == tuple(INACCESSIBLE_SUBNETS)
    assert config.local_network_scan == LOCAL_NETWORK_SCAN
    assert config.subnets == tuple(SUBNETS)


def test_icmp_scan_configuration_schema():
    config = Pydantic___ICMPScanConfiguration(**ICMP_CONFIGURATION)

    assert config.timeout == TIMEOUT


def test_icmp_scan_configuration_schema__negative_timeout():
    negative_timeout_configuration = ICMP_CONFIGURATION.copy()
    negative_timeout_configuration["timeout"] = -1

    with pytest.raises(ValidationError):
        Pydantic___ICMPScanConfiguration(**negative_timeout_configuration)


def test_tcp_scan_configuration_schema():
    config = Pydantic___TCPScanConfiguration(**TCP_SCAN_CONFIGURATION)

    assert config.timeout == TIMEOUT
    assert config.ports == tuple(PORTS)


@pytest.mark.parametrize("ports", INVALID_PORTS)
def test_tcp_scan_configuration_schema__ports_out_of_range(ports):
    invalid_ports_configuration = TCP_SCAN_CONFIGURATION.copy()
    invalid_ports_configuration["ports"] = ports

    with pytest.raises(ValidationError):
        Pydantic___TCPScanConfiguration(**invalid_ports_configuration)


def test_tcp_scan_configuration_schema__negative_timeout():
    negative_timeout_configuration = TCP_SCAN_CONFIGURATION.copy()
    negative_timeout_configuration["timeout"] = -1

    with pytest.raises(ValidationError):
        Pydantic___TCPScanConfiguration(**negative_timeout_configuration)


def test_network_scan_configuration():
    config = Pydantic___NetworkScanConfiguration(**NETWORK_SCAN_CONFIGURATION)

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

    config = Pydantic___ExploitationOptionsConfiguration(**{"http_ports": ports})

    assert config.http_ports == tuple(ports)


@pytest.mark.parametrize("ports", INVALID_PORTS)
def test_exploitation_options_configuration_schema__ports_out_of_range(ports):
    invalid_ports_configuration = {"http_ports": ports}

    with pytest.raises(ValidationError):
        Pydantic___ExploitationOptionsConfiguration(**invalid_ports_configuration)


def test_exploiter_configuration_schema():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}

    config = Pydantic___PluginConfiguration(**{"name": name, "options": options})

    assert config.name == name
    assert config.options == options


def test_exploitation_configuration():
    config = Pydantic___ExploitationConfiguration(**EXPLOITATION_CONFIGURATION)
    config_dict = config.dict()

    assert isinstance(config, Pydantic___ExploitationConfiguration)
    assert config_dict == EXPLOITATION_CONFIGURATION


def test_propagation_configuration():
    config = Pydantic___PropagationConfiguration(**PROPAGATION_CONFIGURATION)
    config_dict = config.dict()

    assert isinstance(config, Pydantic___PropagationConfiguration)
    assert isinstance(config.network_scan, Pydantic___NetworkScanConfiguration)
    assert isinstance(config.exploitation, Pydantic___ExploitationConfiguration)
    assert config.maximum_depth == 5
    assert config_dict == PROPAGATION_CONFIGURATION


def test_propagation_configuration__invalid_maximum_depth():
    negative_maximum_depth_configuration = PROPAGATION_CONFIGURATION.copy()
    negative_maximum_depth_configuration["maximum_depth"] = -1

    with pytest.raises(ValidationError):
        Pydantic___PropagationConfiguration(**negative_maximum_depth_configuration)


def test_agent_configuration():
    config = Pydantic___AgentConfiguration(**AGENT_CONFIGURATION)
    config_dict = config.dict()

    assert isinstance(config, Pydantic___AgentConfiguration)
    assert config.keep_tunnel_open_time == 30
    assert isinstance(config.custom_pbas, Pydantic___CustomPBAConfiguration)
    assert isinstance(config.post_breach_actions[0], Pydantic___PluginConfiguration)
    assert isinstance(config.credential_collectors[0], Pydantic___PluginConfiguration)
    assert isinstance(config.payloads[0], Pydantic___PluginConfiguration)
    assert isinstance(config.propagation, Pydantic___PropagationConfiguration)
    assert config_dict == AGENT_CONFIGURATION


def test_agent_configuration__negative_keep_tunnel_open_time():
    negative_keep_tunnel_open_time_configuration = AGENT_CONFIGURATION.copy()
    negative_keep_tunnel_open_time_configuration["keep_tunnel_open_time"] = -1

    with pytest.raises(InvalidConfigurationError):
        Pydantic___AgentConfiguration(**negative_keep_tunnel_open_time_configuration)


def test_incorrect_type():
    valid_config = Pydantic___AgentConfiguration(**AGENT_CONFIGURATION)
    with pytest.raises(InvalidConfigurationError):
        valid_config_dict = valid_config.__dict__
        valid_config_dict["keep_tunnel_open_time"] = "not_a_float"
        Pydantic___AgentConfiguration(**valid_config_dict)
