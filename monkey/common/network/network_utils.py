from typing import Optional, Tuple


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
