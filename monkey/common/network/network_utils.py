import ipaddress
import socket
from ipaddress import IPv4Address, IPv4Interface
from typing import Iterable, List, Sequence

import ifaddr


def get_my_ip_addresses() -> Sequence[IPv4Address]:
    return [interface.ip for interface in get_network_interfaces()]


def get_network_interfaces() -> List[IPv4Interface]:
    local_interfaces = []
    for adapter in ifaddr.get_adapters():
        for ip in _select_ipv4_ips(adapter.ips):
            interface = ipaddress.IPv4Interface(f"{ip.ip}/{ip.network_prefix}")
            if not interface.ip.is_link_local:
                local_interfaces.append(interface)

    return local_interfaces


def _select_ipv4_ips(ips: Iterable[ifaddr.IP]) -> Iterable[ifaddr.IP]:
    return filter(lambda ip: _is_ipv4(ip) and ip.ip != "127.0.0.1", ips)


def _is_ipv4(ip: ifaddr.IP) -> bool:
    # In ifaddr, IPv4 addresses are strings, while IPv6 addresses are tuples
    return type(ip.ip) is str


def is_local_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
