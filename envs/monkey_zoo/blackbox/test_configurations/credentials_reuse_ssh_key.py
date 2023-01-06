import dataclasses

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from common.credentials import Credentials, Password, Username

from .noop import noop_test_configuration
from .utils import (
    add_credential_collectors,
    add_exploiters,
    add_subnets,
    add_tcp_ports,
    replace_agent_configuration,
    replace_propagation_credentials,
    set_keep_tunnel_open_time,
    set_maximum_depth,
)


# Tests:
#     SSHCollector steals key from machine A(10.2.3.14),
#     then B(10.2.4.15) exploits C(10.2.5.16) with that key
def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    exploiters = [
        PluginConfiguration(name="SSHExploiter", options={}),
    ]

    return add_exploiters(agent_configuration, exploiters=exploiters)


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = ["10.2.3.14", "10.2.4.15", "10.2.5.16"]
    return add_subnets(agent_configuration, subnets)


def _add_credential_collectors(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    credential_collectors = [
        PluginConfiguration(name="SSHCollector", options={}),
    ]

    return add_credential_collectors(
        agent_configuration, credential_collectors=credential_collectors
    )


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [22]
    return add_tcp_ports(agent_configuration, ports)


test_agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 3)
test_agent_configuration = set_keep_tunnel_open_time(test_agent_configuration, 20)
test_agent_configuration = _add_exploiters(test_agent_configuration)
test_agent_configuration = _add_subnets(test_agent_configuration)
test_agent_configuration = _add_credential_collectors(test_agent_configuration)
test_agent_configuration = _add_tcp_ports(test_agent_configuration)

CREDENTIALS = (
    Credentials(identity=Username(username="m0nk3y"), secret=None),
    Credentials(identity=None, secret=Password(password="u26gbVQe")),
    Credentials(identity=None, secret=Password(password="5BuYHeVl")),
)

credentials_reuse_ssh_key_test_configuration = dataclasses.replace(noop_test_configuration)
replace_agent_configuration(
    test_configuration=credentials_reuse_ssh_key_test_configuration,
    agent_configuration=test_agent_configuration,
)
replace_propagation_credentials(
    test_configuration=credentials_reuse_ssh_key_test_configuration,
    propagation_credentials=CREDENTIALS,
)
