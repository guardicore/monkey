from typing import Sequence

from common.types import NetworkPort
from infection_monkey.i_puppet import TargetHost


def all_exploitation_ports_are_closed(host: TargetHost, exploitation_ports: Sequence[int]) -> bool:
    closed_tcp_ports = host.ports_status.tcp_ports.closed
    return all([p in closed_tcp_ports for p in exploitation_ports])


def all_udp_ports_are_closed(host: TargetHost, udp_ports: Sequence[NetworkPort]) -> bool:
    """
    Check if all UDP ports in a given sequence are closed on the host

    :param host: The host to check
    :param udp_ports: The sequence of UDP ports to check
    :return: True if all ports are closed, False otherwise
    """
    closed_udp_ports = host.ports_status.udp_ports.closed
    return all([p in closed_udp_ports for p in udp_ports])
