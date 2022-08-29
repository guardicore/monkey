import itertools
import socket
import struct
from collections import namedtuple
from ipaddress import IPv4Interface
from random import randint  # noqa: DUO102
from typing import List

import netifaces
import psutil

from infection_monkey.utils.environment import is_windows_os

# Timeout for monkey connections
LOOPBACK_NAME = b"lo"
SIOCGIFADDR = 0x8915  # get PA address
SIOCGIFNETMASK = 0x891B  # get network PA mask
RTF_UP = 0x0001  # Route usable
RTF_REJECT = 0x0200

# TODO: We can probably replace both of these namedtuples with classes in Python's ipaddress
#       library: https://docs.python.org/3/library/ipaddress.html
NetworkAddress = namedtuple("NetworkAddress", ("ip", "domain"))


def get_local_network_interfaces() -> List[IPv4Interface]:
    return [IPv4Interface(f"{i['addr']}/{i['netmask']}") for i in get_host_subnets()]


def get_host_subnets():
    """
    Returns a list of subnets visible to host (omitting loopback and auto conf networks)
    Each subnet item contains the host IP in that network + the subnet.
    :return: List of dict, keys are "addr" and "subnet"
    """
    ipv4_nets = [
        netifaces.ifaddresses(interface)[netifaces.AF_INET]
        for interface in netifaces.interfaces()
        if netifaces.AF_INET in netifaces.ifaddresses(interface)
    ]
    # flatten
    ipv4_nets = itertools.chain.from_iterable(ipv4_nets)
    # remove loopback
    ipv4_nets = [network for network in ipv4_nets if network["addr"] != "127.0.0.1"]
    # remove auto conf
    ipv4_nets = [network for network in ipv4_nets if not network["addr"].startswith("169.254")]
    for network in ipv4_nets:
        if "broadcast" in network:
            network.pop("broadcast")
        for attr in network:
            network[attr] = network[attr]
    return ipv4_nets


if is_windows_os():

    def local_ips():
        local_hostname = socket.gethostname()
        return socket.gethostbyname_ex(local_hostname)[2]

    def get_routes():
        raise NotImplementedError()

else:
    from fcntl import ioctl

    def local_ips():
        valid_ips = [network["addr"] for network in get_host_subnets()]
        return valid_ips

    def get_routes():  # based on scapy implementation for route parsing
        try:
            f = open("/proc/net/route", "r")
        except IOError:
            return []
        routes = []
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", LOOPBACK_NAME))
        addrfamily = struct.unpack("h", ifreq[16:18])[0]
        if addrfamily == socket.AF_INET:
            ifreq2 = ioctl(s, SIOCGIFNETMASK, struct.pack("16s16x", LOOPBACK_NAME))
            msk = socket.ntohl(struct.unpack("I", ifreq2[20:24])[0])
            dst = socket.ntohl(struct.unpack("I", ifreq[20:24])[0]) & msk
            ifaddr = socket.inet_ntoa(ifreq[20:24])
            routes.append((dst, msk, "0.0.0.0", LOOPBACK_NAME, ifaddr))

        for line in f.readlines()[1:]:
            iff, dst, gw, flags, x, x, x, msk, x, x, x = [var.encode() for var in line.split()]
            flags = int(flags, 16)
            if flags & RTF_UP == 0:
                continue
            if flags & RTF_REJECT:
                continue
            try:
                ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", iff))
            except IOError:  # interface is present in routing tables but does not have any
                # assigned IP
                ifaddr = "0.0.0.0"
            else:
                addrfamily = struct.unpack("h", ifreq[16:18])[0]
                if addrfamily == socket.AF_INET:
                    ifaddr = socket.inet_ntoa(ifreq[20:24])
                else:
                    continue
            routes.append(
                (
                    socket.htonl(int(dst, 16)) & 0xFFFFFFFF,
                    socket.htonl(int(msk, 16)) & 0xFFFFFFFF,
                    socket.inet_ntoa(struct.pack("I", int(gw, 16))),
                    iff,
                    ifaddr,
                )
            )

        f.close()
        return routes


def get_free_tcp_port(min_range=1024, max_range=65535):
    min_range = max(1, min_range)
    max_range = min(65535, max_range)

    in_use = [conn.laddr[1] for conn in psutil.net_connections()]

    for i in range(min_range, max_range):
        port = randint(min_range, max_range)

        if port not in in_use:
            return port

    return None
