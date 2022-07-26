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
    set_maximum_depth,
)


def _add_exploiters(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    brute_force = [
        PluginConfiguration(name="WmiExploiter", options={"smb_download_timeout": 30}),
    ]

    return add_exploiters(agent_configuration, brute_force=brute_force, vulnerability=[])


def _add_subnets(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    subnets = [
        "10.2.2.14",
        "10.2.2.15",
    ]
    return add_subnets(agent_configuration, subnets)


def _add_credential_collectors(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return add_credential_collectors(
        agent_configuration, [PluginConfiguration("MimikatzCollector", {})]
    )


def _add_tcp_ports(agent_configuration: AgentConfiguration) -> AgentConfiguration:
    ports = [135]
    return add_tcp_ports(agent_configuration, ports)


agent_configuration = set_maximum_depth(noop_test_configuration.agent_configuration, 1)
agent_configuration = _add_exploiters(agent_configuration)
agent_configuration = _add_subnets(agent_configuration)
agent_configuration = _add_credential_collectors(agent_configuration)
agent_configuration = _add_tcp_ports(agent_configuration)
agent_configuration = _add_credential_collectors(agent_configuration)

wmi_mimikatz_test_configuration = replace_agent_configuration(
    noop_test_configuration, agent_configuration
)


CREDENTIALS = (
    Credentials(Username("Administrator"), None),
    Credentials(Username("m0nk3y"), None),
    Credentials(Username("user"), None),
    Credentials(None, Password("Ivrrw5zEzs")),
    Credentials(None, Password("Password1!")),
)
wmi_mimikatz_test_configuration = replace_propagation_credentials(
    wmi_mimikatz_test_configuration, CREDENTIALS
)
