import dataclasses

from common.agent_configuration import AgentConfiguration, PluginConfiguration
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
        PluginConfiguration(name="SmbExploiter", options={"smb_download_timeout": 30}),
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


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 3)
test_agent_configuration = set_keep_tunnel_open_time(test_agent_configuration, 20)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)

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

smb_pth_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=smb_pth_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=smb_pth_test_configuration, propagation_credentials=CREDENTIALS
)
