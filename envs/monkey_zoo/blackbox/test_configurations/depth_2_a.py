import dataclasses
from typing import Dict, Mapping

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, Password, Username, NTHash

from .noop import noop_test_configuration
from .utils import (
    add_exploiters,
    add_fingerprinters,
    add_http_ports,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_maximum_depth,
)

# Tests:
#     SSH password and key brute-force, key stealing (10.2.2.11, 10.2.2.12)
#     Powershell credential reuse (logging in without credentials
#       to an identical user on another machine)(10.2.3.44, 10.2.3.46)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        # Log4Shell is required to hop into 46, which then uses credential reuse on 44.
        # Look at envs/monkey_zoo/docs/network_diagrams/powershell_credential_reuse.drawio.png
        "Log4Shell": {
            # no ports are configured but because `try_all_discovered_http_ports` is
            # set to true, the exploiter should exploit 10.2.3.46 on port 8080 (configured
            # at `agent_configuration.propagation.exploitation.options.http_ports`)
            "try_all_discovered_http_ports": True,
            "target_ports": [],
        },
        "SSH": {},
        "PowerShell": {},
        "RDP": {},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.11",
        "10.2.2.12",
        "10.2.3.44",
        "10.2.3.46",
        "10.2.3.64",
        "10.2.3.65",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_fingerprinters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    fingerprinters = [PluginConfiguration(name="http", options={})]

    return add_fingerprinters(agent_configuration, fingerprinters)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 3389, 5985, 5986, 8080]
    return add_tcp_ports(agent_configuration, ports)


def _add_http_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return add_http_ports(agent_configuration, [8080])


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 2)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_fingerprinters(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)
test_agent_configuration = _add_http_ports(test_agent_configuration)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=None, secret=Password(password="^NgDvY59~8")),
    Credentials(identity=None, secret=Password(password="P@ssw0rd!")),
    Credentials(identity=None, secret=NTHash(nt_hash="68965ABB32F8CE46F7E40075FA5B623E")),
)

depth_2_a_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_2_a_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_2_a_test_configuration, propagation_credentials=CREDENTIALS
)
