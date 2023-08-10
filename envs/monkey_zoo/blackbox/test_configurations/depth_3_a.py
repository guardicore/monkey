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
    set_randomize_agent_hash,
)

# Tests:
#     Powershell (10.2.3.45, 10.2.3.46, 10.2.3.47, 10.2.3.48)
#     Tunneling through grandparent agent (SSH brute force) (10.2.2.9, 10.2.1.10, 10.2.0.11)
#     WMI pass the hash (10.2.2.15)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        "PowerShell": {},
        "SSH": {},
        "WMI": {"agent_binary_upload_timeout": 30},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.9",
        "10.2.3.45",
        "10.2.3.47",
        "10.2.3.48",
        "10.2.1.10",
        "10.2.0.11",
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 135, 5985, 5986]
    return add_tcp_ports(agent_configuration, ports)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 3)
test_agent_configuration = set_keep_tunnel_open_time(test_agent_configuration, 20)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)
test_agent_configuration = set_randomize_agent_hash(test_agent_configuration, True)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=Password(password="Passw0rd!")),
    Credentials(identity=Username(username="m0nk3y-user"), secret=None),
    Credentials(identity=None, secret=Password(password="3Q=(Ge(+&w]*")),
    Credentials(identity=None, secret=Password(password="`))jU7L(w}")),
    Credentials(identity=None, secret=NTHash(nt_hash="d0f0132b308a0c4e5d1029cc06f48692")),
    Credentials(identity=None, secret=NTHash(nt_hash="5da0889ea2081aa79f6852294cba4a5e")),
    Credentials(identity=None, secret=NTHash(nt_hash="50c9987a6bf1ac59398df9f911122c9b")),
    # Hash for Mimikatz-15
    Credentials(identity=None, secret=NTHash(nt_hash="F7E457346F7743DAECE17258667C936D")),
)

depth_3_a_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_3_a_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_3_a_test_configuration, propagation_credentials=CREDENTIALS
)
