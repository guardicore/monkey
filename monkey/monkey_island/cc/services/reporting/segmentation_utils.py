from ipaddress import IPv4Address
from typing import Optional, Sequence

from common.network.network_range import NetworkRange


def get_ip_if_in_subnet(
    ip_addresses: Sequence[IPv4Address], subnet: NetworkRange
) -> Optional[IPv4Address]:
    """

    :param ip_addresses: IP address list
    :param subnet: Subnet to check if one of ip_addresses is in there
    :return: The first IP in ip_addresses which is in the subnet if there is one, otherwise None
    """
    for ip_address in ip_addresses:
        if subnet.is_in_range(ip_address):
            return ip_address
    return None
