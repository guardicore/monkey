import dataclasses
from typing import Dict, Mapping

from common.agent_configuration import AgentConfiguration

from .noop import noop_test_configuration
from .utils import (
    add_exploiters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    set_maximum_depth,
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        "ZerologonExploiter": {},
        "SMBExploiter": {"smb_download_timeout": 30},
    }

    return add_exploiters(agent_configuration, exploiters)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    tcp_ports = [135, 445]
    return add_tcp_ports(agent_configuration, tcp_ports)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = ["10.2.2.25"]
    return add_subnets(agent_configuration, subnets)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)

zerologon_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=zerologon_test_configuration, agent_configuration=test_agent_configuration
)
