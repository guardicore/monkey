from common.configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, Password, Username

from .noop import noop_test_configuration
from .utils import (
    add_credential_collectors,
    add_exploiters,
    add_http_ports,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_maximum_depth,
)

CREDENTIALS = (
    Credentials(Username("m0nk3y"), None),
    Credentials(None, Password("Ivrrw5zEzs")),
    Credentials(None, Password("Xk8VDTsC")),
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [
        PluginConfiguration(name="HadoopExploiter", options={}),
        PluginConfiguration(name="Log4ShellExploiter", options={}),
        PluginConfiguration(name="MSSQLExploiter", options={}),
        PluginConfiguration(name="SmbExploiter", options={}),
        PluginConfiguration(name="SSHExploiter", options={}),
    ]
    vulnerability = [PluginConfiguration(name="ZerologonExploiter", options={})]

    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=vulnerability)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.2",
        "10.2.2.3",
        "10.2.3.55",
        "10.2.3.56",
        "10.2.3.49",
        "10.2.3.50",
        "10.2.3.51",
        "10.2.3.52",
        "10.2.2.16",
        "10.2.2.14",
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_credential_collectors(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return add_credential_collectors(
        agent_configuration, [PluginConfiguration("MimikatzCollector", {})]
    )


HTTP_PORTS = [8080, 8983, 9600]


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 445] + HTTP_PORTS
    return add_tcp_ports(agent_configuration, ports)


def _add_http_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return add_http_ports(agent_configuration, HTTP_PORTS)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
agent_configuration = _add_tcp_ports(agent_configuration)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)
agent_configuration = _add_credential_collectors(agent_configuration)
agent_configuration = _add_http_ports(agent_configuration)

depth_1_a_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)
depth_1_a_test_configuration = replace_propagation_credentials(
    depth_1_a_test_configuration, CREDENTIALS
)
