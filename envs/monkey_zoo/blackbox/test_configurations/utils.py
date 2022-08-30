from typing import Sequence

from common.agent_configuration import AgentConfiguration, PluginConfiguration


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
