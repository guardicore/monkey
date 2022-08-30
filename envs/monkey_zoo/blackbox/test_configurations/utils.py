from dataclasses import replace
from typing import Sequence, Tuple

from common.agent_configuration import (
    AgentConfiguration,
    ExploitationConfiguration,
    ExploitationOptionsConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
)
from common.credentials import Credentials

from . import TestConfiguration


def add_exploiters(
    agent_configuration: AgentConfiguration,
    brute_force: Sequence[PluginConfiguration] = [],
    vulnerability: Sequence[PluginConfiguration] = [],
) -> AgentConfiguration:

    agent_configuration.propagation.exploitation.brute_force = brute_force
    agent_configuration.propagation.exploitation.vulnerability = vulnerability

    return agent_configuration


def add_fingerprinters(
    agent_configuration: AgentConfiguration, fingerprinters: Sequence[PluginConfiguration]
) -> AgentConfiguration:

    agent_configuration.propagation.network_scan.fingerprinters = fingerprinters

    return agent_configuration


def add_tcp_ports(
    agent_configuration: AgentConfiguration, tcp_ports: Sequence[int]
) -> AgentConfiguration:

    agent_configuration.propagation.network_scan.tcp.ports = tuple(tcp_ports)

    return agent_configuration


def add_subnets(
    agent_configuration: AgentConfiguration, subnets: Sequence[str]
) -> AgentConfiguration:

    agent_configuration.propagation.network_scan.targets.subnets = subnets

    return agent_configuration


def add_credential_collectors(
    agent_configuration: AgentConfiguration, credential_collectors: Sequence[PluginConfiguration]
) -> AgentConfiguration:

    agent_configuration.credential_collectors = tuple(credential_collectors)

    return agent_configuration


def add_http_ports(
    agent_configuration: AgentConfiguration, http_ports: Sequence[int]
) -> AgentConfiguration:

    agent_configuration.propagation.exploitation.options.http_ports = http_ports

    return agent_configuration


def set_keep_tunnel_open_time(
    agent_configuration: AgentConfiguration, keep_tunnel_open_time: int
) -> AgentConfiguration:

    agent_configuration.keep_tunnel_open_time = keep_tunnel_open_time

    return agent_configuration


def set_maximum_depth(
    agent_configuration: AgentConfiguration, maximum_depth: int
) -> AgentConfiguration:

    agent_configuration.propagation.maximum_depth = maximum_depth

    return agent_configuration


def replace_exploitation_configuration(
    agent_configuration: AgentConfiguration, exploitation_configuration: ExploitationConfiguration
) -> AgentConfiguration:
    propagation_configuration = replace(
        agent_configuration.propagation, exploitation=exploitation_configuration
    )

    return replace_propagation_configuration(agent_configuration, propagation_configuration)


def replace_scan_target_configuration(
    agent_configuration: AgentConfiguration, scan_target_configuration: ScanTargetConfiguration
) -> AgentConfiguration:
    network_scan_configuration = replace(
        agent_configuration.propagation.network_scan, targets=scan_target_configuration
    )

    return replace_network_scan_configuration(agent_configuration, network_scan_configuration)


def replace_network_scan_configuration(
    agent_configuration: AgentConfiguration, network_scan_configuration: NetworkScanConfiguration
) -> AgentConfiguration:
    propagation_configuration = replace(
        agent_configuration.propagation, network_scan=network_scan_configuration
    )
    return replace_propagation_configuration(agent_configuration, propagation_configuration)


def replace_propagation_configuration(
    agent_configuration: AgentConfiguration, propagation_configuration: PropagationConfiguration
) -> AgentConfiguration:
    return replace(agent_configuration, propagation=propagation_configuration)


def replace_exploitation_options_configuration(
    agent_configuration: AgentConfiguration,
    exploitation_options_configuration: ExploitationOptionsConfiguration,
) -> AgentConfiguration:
    exploitation_configuration = agent_configuration.propagation.exploitation
    exploitation_configuration = replace(
        exploitation_configuration, options=exploitation_options_configuration
    )
    return replace_exploitation_configuration(agent_configuration, exploitation_configuration)


def replace_agent_configuration(
    test_configuration: TestConfiguration, agent_configuration: AgentConfiguration
) -> TestConfiguration:
    return replace(test_configuration, agent_configuration=agent_configuration)


def replace_propagation_credentials(
    test_configuration: TestConfiguration, propagation_credentials: Tuple[Credentials, ...]
):
    return replace(test_configuration, propagation_credentials=propagation_credentials)
