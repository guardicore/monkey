import ipaddress
from ipaddress import IPv4Address, IPv4Interface
from typing import List, Optional, Sequence, Tuple

from netifaces import AF_INET, ifaddresses, interfaces


def get_my_ip_addresses_legacy() -> Sequence[str]:
    return [str(ip) for ip in get_my_ip_addresses()]


def get_my_ip_addresses() -> Sequence[IPv4Address]:
    return [interface.ip for interface in get_network_interfaces()]


def get_network_interfaces() -> List[IPv4Interface]:
    local_interfaces = []
    for interface in interfaces():
        addresses = ifaddresses(interface).get(AF_INET, [])
        local_interfaces.extend(
            [
                ipaddress.IPv4Interface(link["addr"] + "/" + link["netmask"])
                for link in addresses
                if link["addr"] != "127.0.0.1"
            ]
        )
    return local_interfaces


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
