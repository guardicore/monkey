import logging
import socket
import struct
import sys
from ipaddress import IPv4Address, IPv4Interface
from typing import Iterable, Optional

from common.common_consts.timeouts import CONNECTION_TIMEOUT
from infection_monkey.network.info import get_routes

DEFAULT_TIMEOUT = CONNECTION_TIMEOUT
BANNER_READ = 1024

logger = logging.getLogger(__name__)


def get_interface_to_target(
    interfaces: Iterable[IPv4Interface], target: IPv4Address
) -> Optional[IPv4Interface]:
    """
    This function attempts to find the interface that can connect to the target. It first attempts
    to do this rationally by examining network membership. If that fails, it attempts to do this
    empirically by opening sockets and examining routes.

    :param interfaces: An iterable of interfaces
    :param target: The IP address of the target
    :return: The network interface that can connect to the target, or None if no such interface
             could be found
    """

    interface_to_target = _rational_get_interface_to_target(interfaces, target)

    if interface_to_target is not None:
        return interface_to_target

    interface_ip_to_target = _empirical_get_interface_to_target(str(target))

    if interface_ip_to_target is None:
        return None

    for i in interfaces:
        if i.ip == interface_ip_to_target:
            return i

    return None


def _rational_get_interface_to_target(
    interfaces: Iterable[IPv4Interface], target: IPv4Address
) -> Optional[IPv4Interface]:
    """
    This function attempts to find the interface that can connect to the target by looking at the
    system's network membership and the target's IP address. There are some rare edge cases where
    this will be incorrect, but this is an acceptable tradeoff, as other approaches involve opening
    sockets, which can be slow and noisy.

    :param interfaces: An iterable of interfaces
    :param target: The IP address of the target
    :return: The network interface that can connect to the target, or None if no such interface
             could be found
    """
    for i in interfaces:
        if target in i.network:
            return i

    return None


def _empirical_get_interface_to_target(target: str) -> Optional[IPv4Address]:
    """
    This function attempts to find the interface that can connect to the target by opening a socket

    :param target: destination IP address string without port. E.G. '192.168.1.1.'
    :return: IP address string of an interface that can connect to the target, or None if no such
             interface could be found
    """
    if sys.platform == "win32":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((target, 1))
            ip_to_dst = s.getsockname()[0]
        except KeyError:
            logger.debug(
                "Couldn't get an interface to the target, presuming that target is localhost."
            )
            ip_to_dst = "127.0.0.1"
        finally:
            s.close()
        return IPv4Address(ip_to_dst)
    else:
        # based on scapy implementation

        def atol(x):
            ip = socket.inet_aton(x)
            return struct.unpack("!I", ip)[0]

        routes = get_routes()
        target_long = atol(target)
        paths = []
        for d, m, gw, i, a in routes:
            aa = atol(a)
            if aa == target_long:
                paths.append((0xFFFFFFFF, ("lo", a, "0.0.0.0")))
            if (target_long & m) == (d & m):
                paths.append((m, (i, a, gw)))
        if not paths:
            return None
        paths.sort()
        ret = paths[-1][1]
        return IPv4Address(ret[1])
