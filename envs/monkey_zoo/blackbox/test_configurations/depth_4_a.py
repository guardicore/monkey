import dataclasses
from typing import Dict, Mapping

from common.agent_configuration import AgentConfiguration
from common.credentials import Credentials, Password, Username

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
#     Tunneling (SSH brute force) (10.2.2.9, 10.2.1.10, 10.2.0.12, 10.2.0.13)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        "SSH": {},
        "WMI": {"agent_binary_upload_timeout": 30},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.9",
        "10.2.1.10",
        "10.2.0.12",
        "10.2.0.13",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 135, 5985, 5986]
    return add_tcp_ports(agent_configuration, ports)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 4)
test_agent_configuration = set_keep_tunnel_open_time(test_agent_configuration, 20)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=None, secret=Password(password="3Q=(Ge(+&w]*")),
    Credentials(identity=None, secret=Password(password="`))jU7L(w}")),
    Credentials(identity=None, secret=Password(password="prM2qsroTI")),
    Credentials(identity=None, secret=Password(password="t67TC5ZDmz")),
)

depth_4_a_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_4_a_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_4_a_test_configuration, propagation_credentials=CREDENTIALS
)
