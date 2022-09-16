from ipaddress import IPv4Address, IPv4Interface
from typing import Sequence

from ring import lru

from common.network.network_utils import get_my_ip_addresses, get_network_interfaces


@lru(maxsize=1)
def get_cached_local_ip_addresses() -> Sequence[IPv4Address]:
    return get_my_ip_addresses()


# The subnets list should not change often. Therefore, we can cache the result and never call this
# function more than once. This stopgap measure is here since this function is called a lot of times
# during the report generation. This means that if the interfaces or subnets of the Island machine
# change, the Island process needs to be restarted.
@lru(maxsize=1)
def get_cached_local_interfaces() -> Sequence[IPv4Interface]:
    return get_network_interfaces()
