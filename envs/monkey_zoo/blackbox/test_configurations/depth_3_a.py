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

# Tests:
#     Powershell (10.2.3.45, 10.2.3.46, 10.2.3.47, 10.2.3.48)
#     Tunneling (SSH brute force) (10.2.2.9, 10.2.1.10, 10.2.0.12, 10.2.0.11)
#     WMI pass the hash (10.2.2.15)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [
        PluginConfiguration(name="PowerShellExploiter", options={}),
        PluginConfiguration(name="SSHExploiter", options={}),
        PluginConfiguration(name="WmiExploiter", options={"smb_download_timeout": 30}),
    ]

    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=[])


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.9",
        "10.2.3.45",
        "10.2.3.46",
        "10.2.3.47",
        "10.2.3.48",
        "10.2.1.10",
        "10.2.0.12",
        "10.2.0.11",
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 135, 5985, 5986]
    return add_tcp_ports(agent_configuration, ports)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 3)
agent_configuration = set_keep_tunnel_open_time(noop_test_configuration.agent_configuration, 20)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)
agent_configuration = _add_tcp_ports(agent_configuration)

depth_3_a_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)


CREDENTIALS = (
    Credentials(Username("m0nk3y"), None),
    Credentials(Username("m0nk3y-user"), None),
    Credentials(None, Password("Passw0rd!")),
    Credentials(None, Password("3Q=(Ge(+&w]*")),
    Credentials(None, Password("`))jU7L(w}")),
    Credentials(None, Password("t67TC5ZDmz")),
    Credentials(None, NTHash("d0f0132b308a0c4e5d1029cc06f48692")),
    Credentials(None, NTHash("5da0889ea2081aa79f6852294cba4a5e")),
    Credentials(None, NTHash("50c9987a6bf1ac59398df9f911122c9b")),
)
depth_3_a_test_configuration = replace_propagation_credentials(
    depth_3_a_test_configuration, CREDENTIALS
)
