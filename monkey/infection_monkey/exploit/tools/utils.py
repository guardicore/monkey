from typing import Sequence, Set

from common.types import NetworkPort, NetworkService
from infection_monkey.i_puppet import TargetHost


def all_tcp_ports_are_closed(host: TargetHost, tcp_ports: Sequence[NetworkPort]) -> bool:
    closed_tcp_ports = host.ports_status.tcp_ports.closed
    return all([p in closed_tcp_ports for p in tcp_ports])


def all_udp_ports_are_closed(host: TargetHost, udp_ports: Sequence[NetworkPort]) -> bool:
    """
    Check if all UDP ports in a given sequence are closed on the host

    :param host: The host to check
    :param udp_ports: The sequence of UDP ports to check
    :return: True if all ports are closed, False otherwise
    """
    closed_udp_ports = host.ports_status.udp_ports.closed
    return all([p in closed_udp_ports for p in udp_ports])


def any_tcp_port_status_is_unknown(host: TargetHost, tcp_ports: Sequence[NetworkPort]) -> bool:
    all_host_tcp_ports = host.ports_status.tcp_ports
    return any([p not in all_host_tcp_ports for p in tcp_ports])


def get_open_tcp_ports_by_service(host: TargetHost, service: NetworkService) -> Set[NetworkPort]:
    tcp_ports = host.ports_status.tcp_ports
    return {port for port in tcp_ports.open if tcp_ports[port].service == service}
