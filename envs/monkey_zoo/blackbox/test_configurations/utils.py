from typing import Dict, Mapping, Optional, Sequence, Tuple

from monkeytypes import Credentials

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration


def add_exploiters(
    agent_configuration: AgentConfiguration,
    exploiters: Optional[Dict[str, Mapping]],
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    if not exploiters:
        exploiters = {}
    agent_configuration_copy.propagation.exploitation.exploiters = exploiters

    return agent_configuration_copy


def add_fingerprinters(
    agent_configuration: AgentConfiguration, fingerprinters: Sequence[PluginConfiguration]
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    agent_configuration_copy.propagation.network_scan.fingerprinters = fingerprinters

    return agent_configuration_copy


def add_tcp_ports(
    agent_configuration: AgentConfiguration, tcp_ports: Sequence[int]
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    agent_configuration_copy.propagation.network_scan.tcp.ports = tuple(tcp_ports)

    return agent_configuration_copy


def add_subnets(
    agent_configuration: AgentConfiguration, subnets: Sequence[str]
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    agent_configuration_copy.propagation.network_scan.targets.subnets = subnets

    return agent_configuration_copy


def add_credentials_collectors(
    agent_configuration: AgentConfiguration, credentials_collectors: Dict[str, Mapping]
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    agent_configuration_copy.credentials_collectors = credentials_collectors

    return agent_configuration_copy


def set_keep_tunnel_open_time(
    agent_configuration: AgentConfiguration, keep_tunnel_open_time: int
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    agent_configuration_copy.keep_tunnel_open_time = keep_tunnel_open_time

    return agent_configuration_copy


def set_maximum_depth(
    agent_configuration: AgentConfiguration, maximum_depth: int
) -> AgentConfiguration:
    agent_configuration_copy = agent_configuration.copy(deep=True)
    agent_configuration_copy.propagation.maximum_depth = maximum_depth

    return agent_configuration_copy


def set_randomize_agent_hash(agent_configuration: AgentConfiguration, value: bool):
    agent_configuration.polymorphism.randomize_agent_hash = value

    return agent_configuration


def replace_agent_configuration(
    test_configuration: TestConfiguration, agent_configuration: AgentConfiguration
):
    test_configuration.agent_configuration = agent_configuration


def replace_propagation_credentials(
    test_configuration: TestConfiguration, propagation_credentials: Tuple[Credentials, ...]
):
    test_configuration.propagation_credentials = propagation_credentials
