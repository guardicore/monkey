from common.agent_configuration import AgentConfiguration, PluginConfiguration

from .noop import noop_test_configuration
from .utils import (
    add_exploiters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    set_maximum_depth,
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [
        PluginConfiguration(name="PowerShellExploiter", options={}),
    ]

    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=[])


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.3.46",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [5985, 5986]
    return add_tcp_ports(agent_configuration, ports)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)
agent_configuration = _add_tcp_ports(agent_configuration)

powershell_credentials_reuse_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)
