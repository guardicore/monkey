import dataclasses
from typing import Dict, Mapping

from common.agent_configuration import AgentConfiguration
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
    exploiters: Dict[str, Mapping] = {
        "SMBExploiter": {"smb_download_timeout": 30},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


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
    Credentials(identity=Username(username="Administrator"), secret=None),
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=Username(username="user"), secret=None),
    Credentials(identity=None, secret=Password(password="Ivrrw5zEzs")),
    Credentials(identity=None, secret=Password(password="Password1!")),
    Credentials(identity=None, secret=NTHash(nt_hash="d0f0132b308a0c4e5d1029cc06f48692")),
    Credentials(identity=None, secret=NTHash(nt_hash="5da0889ea2081aa79f6852294cba4a5e")),
    Credentials(identity=None, secret=NTHash(nt_hash="50c9987a6bf1ac59398df9f911122c9b")),
)

smb_pth_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=smb_pth_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=smb_pth_test_configuration, propagation_credentials=CREDENTIALS
)
