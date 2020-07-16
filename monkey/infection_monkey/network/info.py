import ipaddress
import itertools
import socket
import struct
from random import randint
from subprocess import check_output

import netifaces
import psutil
import requests
from requests import ConnectionError

from common.network.network_range import CidrRange
from infection_monkey.utils.environment import is_windows_os

# Timeout for monkey connections
TIMEOUT = 15
LOOPBACK_NAME = b"lo"
SIOCGIFADDR = 0x8915  # get PA address
SIOCGIFNETMASK = 0x891b  # get network PA mask
RTF_UP = 0x0001  # Route usable
RTF_REJECT = 0x0200


def get_host_subnets():
    """
    Returns a list of subnets visible to host (omitting loopback and auto conf networks)
    Each subnet item contains the host IP in that network + the subnet.
    :return: List of dict, keys are "addr" and "subnet"
    """
    ipv4_nets = [netifaces.ifaddresses(interface)[netifaces.AF_INET]
                 for interface in netifaces.interfaces()
                 if netifaces.AF_INET in netifaces.ifaddresses(interface)
                 ]
    # flatten
    ipv4_nets = itertools.chain.from_iterable(ipv4_nets)
    # remove loopback
    ipv4_nets = [network for network in ipv4_nets if network['addr'] != '127.0.0.1']
    # remove auto conf
    ipv4_nets = [network for network in ipv4_nets if not network['addr'].startswith('169.254')]
    for network in ipv4_nets:
        if 'broadcast' in network:
            network.pop('broadcast')
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
        valid_ips = [network['addr'] for network in get_host_subnets()]
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

        for l in f.readlines()[1:]:
            iff, dst, gw, flags, x, x, x, msk, x, x, x = [var.encode() for var in l.split()]
            flags = int(flags, 16)
            if flags & RTF_UP == 0:
                continue
            if flags & RTF_REJECT:
                continue
            try:
                ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", iff))
            except IOError:  # interface is present in routing tables but does not have any assigned IP
                ifaddr = "0.0.0.0"
            else:
                addrfamily = struct.unpack("h", ifreq[16:18])[0]
                if addrfamily == socket.AF_INET:
                    ifaddr = socket.inet_ntoa(ifreq[20:24])
                else:
                    continue
            routes.append((socket.htonl(int(dst, 16)) & 0xffffffff,
                           socket.htonl(int(msk, 16)) & 0xffffffff,
                           socket.inet_ntoa(struct.pack("I", int(gw, 16))),
                           iff, ifaddr))

        f.close()
        return routes


def get_free_tcp_port(min_range=1000, max_range=65535):
    start_range = min(1, min_range)
    max_range = min(65535, max_range)

    in_use = [conn.laddr[1] for conn in psutil.net_connections()]

    for i in range(min_range, max_range):
        port = randint(start_range, max_range)

        if port not in in_use:
            return port

    return None


def check_internet_access(services):
    """
    Checks if any of the services are accessible, over HTTPS
    :param services: List of IPs/hostnames
    :return: boolean depending on internet access
    """
    for host in services:
        try:
            requests.get("https://%s" % (host,), timeout=TIMEOUT, verify=False)  # noqa: DUO123
            return True
        except ConnectionError:
            # Failed connecting
            pass

    return False


def get_interfaces_ranges():
    """
    Returns a list of IPs accessible in the host in each network interface, in the subnet.
    Limits to a single class C if the network is larger
    :return: List of IPs, marked as strings.
    """
    res = []
    ifs = get_host_subnets()
    for net_interface in ifs:
        address_str = net_interface['addr']
        netmask_str = net_interface['netmask']
        ip_interface = ipaddress.ip_interface("%s/%s" % (address_str, netmask_str))
        # limit subnet scans to class C only
        res.append(CidrRange(cidr_range="%s/%s" % (address_str, netmask_str)))
    return res


if is_windows_os():
    def get_ip_for_connection(target_ip):
        return None
else:
    def get_ip_for_connection(target_ip):
        try:
            query_str = 'ip route get %s' % target_ip
            resp = check_output(query_str.split())
            substr = resp.split()
            src = substr[substr.index('src') + 1]
            return src
        except Exception:
            return None
