import ipaddress
from ipaddress import IPv4Interface
from typing import List, Optional, Sequence, Tuple

from netifaces import AF_INET, ifaddresses, interfaces


def get_local_ip_addresses() -> Sequence[str]:
    ip_list = []
    for interface in interfaces():
        addresses = ifaddresses(interface).get(AF_INET, [])
        ip_list.extend([link["addr"] for link in addresses if link["addr"] != "127.0.0.1"])
    return ip_list


def get_local_interfaces() -> List[IPv4Interface]:
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
