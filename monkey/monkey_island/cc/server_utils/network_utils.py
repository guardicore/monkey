import ipaddress
from typing import Sequence

from netifaces import AF_INET, ifaddresses, interfaces
from ring import lru

# TODO: This functionality is duplicated in the agent. Unify them after 2216-tcp-relay is merged


# The local IP addresses list should not change often. Therefore, we can cache the result and never
# call this function more than once. This stopgap measure is here since this function is called a
# lot of times during the report generation. This means that if the interfaces of the Island machine
# change, the Island process needs to be restarted.
@lru(maxsize=1)
def get_ip_addresses() -> Sequence[str]:
    ip_list = []
    for interface in interfaces():
        addresses = ifaddresses(interface).get(AF_INET, [])
        ip_list.extend([link["addr"] for link in addresses if link["addr"] != "127.0.0.1"])
    return ip_list


# The subnets list should not change often. Therefore, we can cache the result and never call this
# function more than once. This stopgap measure is here since this function is called a lot of times
# during the report generation. This means that if the interfaces or subnets of the Island machine
# change, the Island process needs to be restarted.
@lru(maxsize=1)
def get_subnets():
    subnets = []
    for interface in interfaces():
        addresses = ifaddresses(interface).get(AF_INET, [])
        subnets.extend(
            [
                ipaddress.ip_interface(link["addr"] + "/" + link["netmask"]).network
                for link in addresses
                if link["addr"] != "127.0.0.1"
            ]
        )
    return subnets
