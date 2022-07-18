from common.configuration import AgentConfiguration, PluginConfiguration

from .noop import noop_test_configuration
from .utils import (
    add_exploiters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    set_maximum_depth,
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [PluginConfiguration(name="SmbExploiter", options={})]
    vulnerability = [PluginConfiguration(name="ZerologonExploiter", options={})]

    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=vulnerability)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    tcp_ports = [135, 445]
    return add_tcp_ports(agent_configuration, tcp_ports)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = ["10.2.2.25"]
    return add_subnets(agent_configuration, subnets)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_tcp_ports(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)

zerologon_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)
