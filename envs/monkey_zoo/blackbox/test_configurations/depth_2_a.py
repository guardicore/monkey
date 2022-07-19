from common.configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, Password, Username

from .noop import noop_test_configuration
from .utils import (
    add_exploiters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_maximum_depth,
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [
        PluginConfiguration(name="SSHExploiter", options={}),
    ]
    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=[])


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.11",
        "10.2.2.12",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22]
    return add_tcp_ports(agent_configuration, ports)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 2)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)
agent_configuration = _add_tcp_ports(agent_configuration)

depth_2_a_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)


CREDENTIALS = (
    Credentials(Username("m0nk3y"), None),
    Credentials(None, Password("^NgDvY59~8")),
)
depth_2_a_test_configuration = replace_propagation_credentials(
    depth_2_a_test_configuration, CREDENTIALS
)
