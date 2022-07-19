from common.configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, NTHash, Password, Username

from .noop import noop_test_configuration
from .utils import (
    add_exploiters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_keep_tunnel_open_time,
    set_maximum_depth,
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [
        PluginConfiguration(name="SmbExploiter", options={}),
    ]

    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=[])


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [445]
    return add_tcp_ports(agent_configuration, ports)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 3)
agent_configuration = set_keep_tunnel_open_time(noop_test_configuration.agent_configuration, 20)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)
agent_configuration = _add_tcp_ports(agent_configuration)

smb_pth_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)


CREDENTIALS = (
    Credentials(Username("Administrator"), None),
    Credentials(Username("m0nk3y"), None),
    Credentials(Username("user"), None),
    Credentials(None, Password("Ivrrw5zEzs")),
    Credentials(None, Password("Password1!")),
    Credentials(None, NTHash("d0f0132b308a0c4e5d1029cc06f48692")),
    Credentials(None, NTHash("5da0889ea2081aa79f6852294cba4a5e")),
    Credentials(None, NTHash("50c9987a6bf1ac59398df9f911122c9b")),
)
smb_pth_test_configuration = replace_propagation_credentials(
    smb_pth_test_configuration, CREDENTIALS
)
