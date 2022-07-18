from dataclasses import replace
from typing import Sequence

from common.configuration import (
    AgentConfiguration,
    ExploitationConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
)

from . import TestConfiguration


def add_exploiters(
    agent_configuration: AgentConfiguration,
    brute_force: Sequence[PluginConfiguration] = [],
    vulnerability: Sequence[PluginConfiguration] = [],
) -> AgentConfiguration:
    exploitation_configuration = replace(
        agent_configuration.propagation.exploitation,
        brute_force=brute_force,
        vulnerability=vulnerability,
    )
    return replace_exploitation_configuration(agent_configuration, exploitation_configuration)


def add_tcp_ports(
    agent_configuration: AgentConfiguration, tcp_ports: Sequence[int]
) -> AgentConfiguration:
    tcp_scan_configuration = replace(
        agent_configuration.propagation.network_scan.tcp, ports=tuple(tcp_ports)
    )
    network_scan_configuration = replace(
        agent_configuration.propagation.network_scan, tcp=tcp_scan_configuration
    )

    return replace_network_scan_configuration(agent_configuration, network_scan_configuration)


def add_subnets(
    agent_configuration: AgentConfiguration, subnets: Sequence[str]
) -> AgentConfiguration:
    scan_target_configuration = replace(
        agent_configuration.propagation.network_scan.targets, subnets=subnets
    )
    return replace_scan_target_configuration(agent_configuration, scan_target_configuration)


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


def replace_agent_configuration(
    test_configuration: TestConfiguration, agent_configuration: AgentConfiguration
) -> TestConfiguration:
    return replace(test_configuration, agent_configuration=agent_configuration)
