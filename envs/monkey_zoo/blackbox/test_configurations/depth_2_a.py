import dataclasses
from typing import Any, Dict, Mapping

from monkeytypes import Credentials, Password, Username

from common.agent_configuration import AgentConfiguration

from .noop import noop_test_configuration
from .utils import (
    add_credentials_collectors,
    add_exploiters,
    add_fingerprinters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_keep_tunnel_open_time,
    set_maximum_depth,
)

# Tests:
#     SSH password and key brute-force, key stealing (10.2.2.11, 10.2.2.12)
#     SMB mimikatz password stealing and brute force (10.2.2.14 and 10.2.2.15)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        "SSH": {},
        "SMB": {"agent_binary_upload_timeout": 30, "smb_connect_timeout": 15},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_credentials_collectors(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    credentials_collectors: Dict[str, Mapping] = {"Mimikatz": {}, "SSH": {}}
    return add_credentials_collectors(
        agent_configuration, credentials_collectors=credentials_collectors
    )


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.11",
        "10.2.2.12",
        "10.2.2.14",
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_fingerprinters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    fingerprinters: Dict[str, Dict[str, Any]] = {
        "smb": {},
        "ssh": {},
    }

    return add_fingerprinters(agent_configuration, fingerprinters)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 135, 445]
    return add_tcp_ports(agent_configuration, ports)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 2)
test_agent_configuration = set_keep_tunnel_open_time(test_agent_configuration, 20)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_fingerprinters(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)
test_agent_configuration = _add_credentials_collectors(test_agent_configuration)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=None, secret=Password(password="^NgDvY59~8")),
    Credentials(identity=None, secret=Password(password="Ivrrw5zEzs")),
)

depth_2_a_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_2_a_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_2_a_test_configuration, propagation_credentials=CREDENTIALS
)
