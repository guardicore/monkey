from typing import Sequence

from infection_monkey.i_puppet import TargetHost


def all_exploitation_ports_are_closed(host: TargetHost, exploitation_ports: Sequence[int]) -> bool:
    closed_tcp_ports = host.ports_status.tcp_ports.closed
    return all([p in closed_tcp_ports for p in exploitation_ports])
