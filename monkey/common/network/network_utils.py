import ipaddress
from ipaddress import IPv4Address, IPv4Interface
from typing import Iterable, List, Optional, Sequence, Tuple

import ifaddr


def get_my_ip_addresses() -> Sequence[IPv4Address]:
    return [interface.ip for interface in get_network_interfaces()]


def get_network_interfaces() -> List[IPv4Interface]:
    local_interfaces = []
    for adapter in ifaddr.get_adapters():
        for ip in _select_ipv4_ips(adapter.ips):
            local_interfaces.append(ipaddress.IPv4Interface(f"{ip.ip}/{ip.network_prefix}"))

    return local_interfaces


def _select_ipv4_ips(ips: Iterable[ifaddr.IP]) -> Iterable[ifaddr.IP]:
    return filter(lambda ip: _is_ipv4(ip) and ip.ip != "127.0.0.1", ips)


def _is_ipv4(ip: ifaddr.IP) -> bool:
    # In ifaddr, IPv4 addresses are strings, while IPv6 addresses are tuples
    return type(ip.ip) is str


# TODO: `address_to_port()` should return the port as an integer.
def address_to_ip_port(address: str) -> Tuple[str, Optional[str]]:
    """
    Split a string containing an IP address (and optionally a port) into IP and Port components.
    Currently only works for IPv4 addresses.

    :param address: The address string.
    :return: Tuple of IP and port strings. The port may be None if no port was in the address.
    """
    if ":" in address:
        ip, port = address.split(":")
        return ip, port or None
    else:
        return address, None
