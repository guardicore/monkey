import dataclasses
from typing import Dict, Mapping

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, Password, Username

from .noop import noop_test_configuration
from .utils import (
    add_credential_collectors,
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
#     Hadoop (10.2.2.2, 10.2.2.3)
#     Log4shell (10.2.3.55, 10.2.3.56, 10.2.3.49, 10.2.3.50, 10.2.3.51, 10.2.3.52)
#     MSSQL (10.2.2.16)
#     SMB mimikatz password stealing and brute force (10.2.2.14 and 10.2.2.15)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        "Hadoop": {
            "target_ports": [8088],
            "request_timeout": 15,
            "agent_binary_download_timeout": 60,
            "yarn_application_suffix": "M0NK3Y3XPL01T",
        },
        "Log4ShellExploiter": {},
        "MSSQLExploiter": {},
        "SMBExploiter": {"smb_download_timeout": 30},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_fingerprinters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    fingerprinters = [PluginConfiguration(name="http", options={})]

    return add_fingerprinters(agent_configuration, fingerprinters)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.2",
        "10.2.2.3",
        "10.2.3.55",
        "10.2.3.56",
        "10.2.3.49",
        "10.2.3.50",
        "10.2.3.51",
        "10.2.3.52",
        "10.2.2.16",
        "10.2.2.14",
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_credential_collectors(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return add_credential_collectors(
        agent_configuration, [PluginConfiguration(name="MimikatzCollector", options={})]
    )


HTTP_PORTS = [8080, 8983, 9600]


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 445] + HTTP_PORTS
    return add_tcp_ports(agent_configuration, ports)


def _add_http_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return add_http_ports(agent_configuration, HTTP_PORTS)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_fingerprinters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)
test_agent_configuration = _add_credential_collectors(test_agent_configuration)
test_agent_configuration = _add_http_ports(test_agent_configuration)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=None, secret=Password(password="Ivrrw5zEzs")),
    Credentials(identity=None, secret=Password(password="Xk8VDTsC")),
)

depth_1_a_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_1_a_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_1_a_test_configuration, propagation_credentials=CREDENTIALS
)
