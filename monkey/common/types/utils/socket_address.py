from ipaddress import IPv4Address

from common.network.network_utils import address_to_ip_port
from common.types import SocketAddress


def socketaddress_from_string(address_str: str) -> SocketAddress:
    """
    Parse a SocketAddress object from a string

    :param address_str: A string of ip:port
    :raises ValueError: If the string is not a valid ip:port
    :return: SocketAddress with the IP and port
    """
    ip, port = address_to_ip_port(address_str)
    if port is None:
        raise ValueError("SocketAddress requires a port")
    return SocketAddress(ip=IPv4Address(ip), port=int(port))
