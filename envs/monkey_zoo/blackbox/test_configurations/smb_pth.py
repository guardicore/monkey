import dataclasses
from typing import Dict, Mapping

from monkeytypes import Credentials, NTHash, Password, Username

from common.agent_configuration import AgentConfiguration

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
        "SMB": {"agent_binary_upload_timeout": 30, "smb_connect_timeout": 15},
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
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=Username(username="unused"), secret=None),
    Credentials(identity=None, secret=Password(password="Unused")),
    Credentials(identity=None, secret=NTHash(nt_hash="F7E457346F7743DAECE17258667C936D")),
)

smb_pth_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=smb_pth_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=smb_pth_test_configuration, propagation_credentials=CREDENTIALS
)
