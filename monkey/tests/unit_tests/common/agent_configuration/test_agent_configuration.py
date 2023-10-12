import pytest
from tests.common.example_agent_configuration import (
    AGENT_CONFIGURATION,
    BLOCKED_IPS,
    EXPLOITATION_CONFIGURATION,
    FINGERPRINTERS,
    ICMP_CONFIGURATION,
    INACCESSIBLE_SUBNETS,
    NETWORK_SCAN_CONFIGURATION,
    PLUGIN_CONFIGURATION,
    PLUGIN_NAME,
    PLUGIN_OPTIONS,
    PORTS,
    PROPAGATION_CONFIGURATION,
    SCAN_MY_NETWORKS,
    SCAN_TARGET_CONFIGURATION,
    SUBNETS,
    TCP_SCAN_CONFIGURATION,
    TIMEOUT,
)

from common.agent_configuration.agent_configuration import AgentConfiguration
from common.agent_configuration.agent_sub_configurations import (
    ExploitationConfiguration,
    ExploitationOptionsConfiguration,
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
    TCPScanConfiguration,
)

INVALID_PORTS = [[-1, 1, 2], [1, 2, 99999]]


def test_build_plugin_configuration():
    config = PluginConfiguration(**PLUGIN_CONFIGURATION)

    assert config.name == PLUGIN_NAME
    assert config.options == PLUGIN_OPTIONS


def test_scan_target_configuration():
    config = ScanTargetConfiguration(**SCAN_TARGET_CONFIGURATION)

    assert config.blocked_ips == tuple(BLOCKED_IPS)
    assert config.inaccessible_subnets == tuple(INACCESSIBLE_SUBNETS)
    assert config.scan_my_networks == SCAN_MY_NETWORKS
    assert config.subnets == tuple(SUBNETS)


@pytest.mark.parametrize(
    "invalid_blocked_ip_list, error", [(["abc"], ValueError), ([1], TypeError)]
)
def test_scan_target_configuration__invalid_blocked_ips(invalid_blocked_ip_list, error):
    invalid_blocked_ips = SCAN_TARGET_CONFIGURATION.copy()
    invalid_blocked_ips["blocked_ips"] = invalid_blocked_ip_list

    with pytest.raises(error):
        ScanTargetConfiguration(**invalid_blocked_ips)


@pytest.mark.parametrize(
    "invalid_inaccessible_subnets_list", [["1-2-3"], ["0.0.0.0/33"], ["www.invalid-.com"]]
)
def test_scan_target_configuration__invalid_inaccessible_subnets(invalid_inaccessible_subnets_list):
    invalid_inaccessible_subnets = SCAN_TARGET_CONFIGURATION.copy()
    invalid_inaccessible_subnets["inaccessible_subnets"] = invalid_inaccessible_subnets_list

    with pytest.raises(ValueError):
        ScanTargetConfiguration(**invalid_inaccessible_subnets)


@pytest.mark.parametrize("invalid_subnets_list", [["1-2-3"], ["0.0.0.0/33"], ["www.invalid-.com"]])
def test_scan_target_configuration__invalid_subnets(invalid_subnets_list):
    invalid_subnets = SCAN_TARGET_CONFIGURATION.copy()
    invalid_subnets["subnets"] = invalid_subnets_list

    with pytest.raises(ValueError):
        ScanTargetConfiguration(**invalid_subnets)


def test_icmp_scan_configuration_schema():
    config = ICMPScanConfiguration(**ICMP_CONFIGURATION)

    assert config.timeout == TIMEOUT


def test_icmp_scan_configuration_schema__negative_timeout():
    negative_timeout_configuration = ICMP_CONFIGURATION.copy()
    negative_timeout_configuration["timeout"] = -1

    with pytest.raises(ValueError):
        ICMPScanConfiguration(**negative_timeout_configuration)


def test_tcp_scan_configuration_schema():
    config = TCPScanConfiguration(**TCP_SCAN_CONFIGURATION)

    assert config.timeout == TIMEOUT
    assert config.ports == tuple(PORTS)


@pytest.mark.parametrize("ports", INVALID_PORTS)
def test_tcp_scan_configuration_schema__ports_out_of_range(ports):
    invalid_ports_configuration = TCP_SCAN_CONFIGURATION.copy()
    invalid_ports_configuration["ports"] = ports

    with pytest.raises(ValueError):
        TCPScanConfiguration(**invalid_ports_configuration)


def test_tcp_scan_configuration_schema__negative_timeout():
    negative_timeout_configuration = TCP_SCAN_CONFIGURATION.copy()
    negative_timeout_configuration["timeout"] = -1

    with pytest.raises(ValueError):
        TCPScanConfiguration(**negative_timeout_configuration)


def test_network_scan_configuration():
    config = NetworkScanConfiguration(**NETWORK_SCAN_CONFIGURATION)

    assert config.tcp.ports == tuple(TCP_SCAN_CONFIGURATION["ports"])
    assert config.tcp.timeout == TCP_SCAN_CONFIGURATION["timeout"]
    assert config.icmp.timeout == ICMP_CONFIGURATION["timeout"]
    assert config.fingerprinters[0].name == FINGERPRINTERS[0]["name"]
    assert config.fingerprinters[0].options == FINGERPRINTERS[0]["options"]
    assert config.targets.blocked_ips == tuple(BLOCKED_IPS)
    assert config.targets.inaccessible_subnets == tuple(INACCESSIBLE_SUBNETS)
    assert config.targets.scan_my_networks == SCAN_MY_NETWORKS
    assert config.targets.subnets == tuple(SUBNETS)


def test_exploitation_options_configuration_schema():
    ports = [0, 1, 2, 3]

    config = ExploitationOptionsConfiguration(http_ports=ports)

    assert config.http_ports == tuple(ports)


@pytest.mark.parametrize("ports", INVALID_PORTS)
def test_exploitation_options_configuration_schema__ports_out_of_range(ports):
    with pytest.raises(ValueError):
        ExploitationOptionsConfiguration(http_ports=ports)


def test_exploiter_configuration_schema():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}

    config = PluginConfiguration(name=name, options=options)

    assert config.name == name
    assert config.options == options


def test_exploitation_configuration():
    config = ExploitationConfiguration(**EXPLOITATION_CONFIGURATION)
    config_dict = config.model_dump(mode="json")

    assert isinstance(config, ExploitationConfiguration)
    assert config_dict == EXPLOITATION_CONFIGURATION


def test_propagation_configuration():
    config = PropagationConfiguration(**PROPAGATION_CONFIGURATION)
    config_dict = config.model_dump(mode="json")

    assert isinstance(config, PropagationConfiguration)
    assert isinstance(config.network_scan, NetworkScanConfiguration)
    assert isinstance(config.exploitation, ExploitationConfiguration)
    assert config.maximum_depth == 5
    assert config_dict == PROPAGATION_CONFIGURATION


def test_propagation_configuration__invalid_maximum_depth():
    negative_maximum_depth_configuration = PROPAGATION_CONFIGURATION.copy()
    negative_maximum_depth_configuration["maximum_depth"] = -1

    with pytest.raises(ValueError):
        PropagationConfiguration(**negative_maximum_depth_configuration)


def test_propagation_configuration__maximum_depth_zero():
    maximum_depth_zero_configuration = PROPAGATION_CONFIGURATION.copy()
    maximum_depth_zero_configuration["maximum_depth"] = 0

    pc = PropagationConfiguration(**maximum_depth_zero_configuration)

    assert pc.maximum_depth == 0


def test_agent_configuration():
    config = AgentConfiguration(**AGENT_CONFIGURATION)
    config_dict = config.model_dump(mode="json")

    assert isinstance(config, AgentConfiguration)
    assert config.keep_tunnel_open_time == 30
    assert isinstance(config.credentials_collectors, dict)
    assert isinstance(config.payloads, dict)
    assert isinstance(config.propagation, PropagationConfiguration)
    assert config_dict == AGENT_CONFIGURATION


def test_agent_configuration__negative_keep_tunnel_open_time_zero():
    keep_tunnel_open_time_zero_configuration = AGENT_CONFIGURATION.copy()
    keep_tunnel_open_time_zero_configuration["keep_tunnel_open_time"] = 0

    ac = AgentConfiguration(**keep_tunnel_open_time_zero_configuration)

    assert ac.keep_tunnel_open_time == 0


def test_agent_configuration__keep_tunnel_open_time():
    negative_keep_tunnel_open_time_configuration = AGENT_CONFIGURATION.copy()
    negative_keep_tunnel_open_time_configuration["keep_tunnel_open_time"] = -1

    with pytest.raises(ValueError):
        AgentConfiguration(**negative_keep_tunnel_open_time_configuration)


def test_incorrect_value():
    valid_config = AgentConfiguration(**AGENT_CONFIGURATION)
    with pytest.raises(ValueError):
        valid_config_dict = valid_config.__dict__
        valid_config_dict["keep_tunnel_open_time"] = "not_a_float"
        AgentConfiguration(**valid_config_dict)
