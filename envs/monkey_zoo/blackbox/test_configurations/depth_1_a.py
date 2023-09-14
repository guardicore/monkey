import dataclasses
from typing import Dict, Mapping

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, NTHash, Password, Username

from .noop import noop_test_configuration
from .utils import (
    add_credentials_collectors,
    add_exploiters,
    add_fingerprinters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_maximum_depth,
    set_randomize_agent_hash,
)

# Tests:
#     Hadoop (10.2.2.2, 10.2.2.3)
#     Log4shell (10.2.3.55, 10.2.3.56, 10.2.3.49, 10.2.3.50, 10.2.3.51, 10.2.3.52)
#     MSSQL (10.2.2.16)
#     SNMP (10.2.3.20)
#     WMI pass the hash (10.2.2.15)
#     Chrome credentials stealing (10.2.3.66 - Windows exploited by RDP, Chrome browser
#                                  10.2.3.67 - Linux exploited by SSH, Chromium browser files)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters: Dict[str, Mapping] = {
        "Hadoop": {
            "target_ports": [8088],
            "request_timeout": 15,
            "agent_binary_download_timeout": 60,
            "yarn_application_suffix": "M0NK3Y3XPL01T",
        },
        "Log4Shell": {},
        "MSSQL": {
            "target_ports": [1433],
            "try_discovered_mssql_ports": False,
            "try_unknown_service_ports": False,
            "server_timeout": 15,
            "agent_binary_download_timeout": 60,
        },
        "SNMP": {
            "snmp_request_timeout": 0.5,
            "snmp_retries": 1,
        },
        "WMI": {"agent_binary_upload_timeout": 30},
        "SSH": {},
        "RDP": {},
    }

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_fingerprinters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    fingerprinters = [
        PluginConfiguration(name="http", options={}),
        PluginConfiguration(name="mssql", options={}),
    ]

    return add_fingerprinters(agent_configuration, fingerprinters)


def _add_credentials_collectors(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    credentials_collectors: Dict[str, Mapping] = {"Chrome": {}}
    return add_credentials_collectors(
        agent_configuration, credentials_collectors=credentials_collectors
    )


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
        "10.2.2.15",
        "10.2.2.16",
        "10.2.3.20",
        "10.2.3.66",
        "10.2.3.67",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22, 445]
    return add_tcp_ports(agent_configuration, ports)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_fingerprinters(test_agent_configuration)
test_agent_configuration = _add_credentials_collectors(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)
test_agent_configuration = set_randomize_agent_hash(test_agent_configuration, True)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=Username(username="c0mmun1ty"), secret=None),
    Credentials(identity=None, secret=Password(password="Xk8VDTsC")),
    # Hash for Mimikatz-15
    Credentials(identity=None, secret=NTHash(nt_hash="F7E457346F7743DAECE17258667C936D")),
    Credentials(identity=Username(username="m0nk3y"), secret=Password(password="P@ssw0rd!")),
    Credentials(identity=Username(username="m0nk3y"), secret=Password(password="password")),
)

depth_1_a_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=depth_1_a_test_configuration, agent_configuration=test_agent_configuration
)
replace_propagation_credentials(
    test_configuration=depth_1_a_test_configuration, propagation_credentials=CREDENTIALS
)
