import ipaddress
from ipaddress import IPv4Address, IPv4Interface
from typing import Iterable, List, Optional, Sequence

import ifaddr
import psutil


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


def port_is_used(
    port: int,
    ip_addresses: Optional[Sequence[IPv4Address]],
) -> bool:
    connections = get_connections([port], ip_addresses)
    return len(connections) > 0


def get_connections(
    ports: Optional[Sequence[int]] = None,
    ip_addresses: Optional[Sequence[IPv4Address]] = None,
) -> List[psutil._common.sconn]:
    connections = psutil.net_connections()
    if ports:
        connections = [connection for connection in connections if connection.laddr.port in ports]
    if ip_addresses:
        ip_addresses_ = list(map(str, ip_addresses))
        connections = [
            connection for connection in connections if connection.laddr.ip in ip_addresses_
        ]
    return connections
