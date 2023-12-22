import dataclasses
from typing import Any, Dict, Mapping

from monkeytypes import Credentials, NTHash, Password, Username

from common.agent_configuration import AgentConfiguration

from .noop import noop_test_configuration
from .utils import (
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
#     Powershell credential reuse (logging in without credentials
#       to an identical user on another machine)(10.2.3.44, 10.2.3.46)
#     RDP double hop (10.2.3.64, 10.2.3.65)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        # Log4Shell is required to hop into 46, which then uses credential reuse on 44.
        # Look at envs/monkey_zoo/docs/network_diagrams/powershell_credential_reuse.drawio.png
        "Log4Shell": {
            # no ports are configured but because `try_all_discovered_http_ports` is
            # set to true, the exploiter should exploit 10.2.3.46 on port 8080 (configured
            # in the HTTP fingerprinter)
            "try_all_discovered_http_ports": True,
            "target_ports": [],
        },
        "PowerShell": {},
        "RDP": {},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.3.44",
        "10.2.3.46",
        "10.2.3.64",
        "10.2.3.65",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_fingerprinters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    fingerprinters: Dict[str, Dict[str, Any]] = {
        "http": {"http_ports": [8080]},
    }

    return add_fingerprinters(agent_configuration, fingerprinters)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [3389, 5985, 5986, 8080]
    return add_tcp_ports(agent_configuration, ports)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 2)
test_agent_configuration = set_keep_tunnel_open_time(test_agent_configuration, 20)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_fingerprinters(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=None, secret=Password(password="P@ssw0rd!")),
    Credentials(identity=None, secret=NTHash(nt_hash="68965ABB32F8CE46F7E40075FA5B623E")),
)

depth_2_b_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_2_b_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_2_b_test_configuration, propagation_credentials=CREDENTIALS
)
