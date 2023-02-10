import logging
import select
import socket
import struct
import sys
from ipaddress import IPv4Address
from typing import Optional

from common.common_consts.timeouts import CONNECTION_TIMEOUT
from infection_monkey.network.info import get_routes

DEFAULT_TIMEOUT = CONNECTION_TIMEOUT
BANNER_READ = 1024

logger = logging.getLogger(__name__)


def check_tcp_port(ip: IPv4Address, port: int, timeout=DEFAULT_TIMEOUT, get_banner=False):
    """
    Checks if a given TCP port is open
    :param ip: Target IP
    :param port: Target Port
    :param timeout: Timeout for socket connection
    :param get_banner:  if true, pulls first BANNER_READ bytes from the socket.
    :return: Tuple, T/F + banner if requested.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((str(ip), port))
    except socket.timeout:
        return False, None
    except socket.error as exc:
        logger.debug("Check port: %s:%s, Exception: %s", ip, port, exc)
        return False, None

    banner = None

    try:
        if get_banner:
            read_ready, _, _ = select.select([sock], [], [], timeout)
            if len(read_ready) > 0:
                banner = sock.recv(BANNER_READ).decode()
    except socket.error:
        pass

    sock.close()
    return True, banner


def tcp_port_to_service(port):
    return "tcp-" + str(port)


def get_interface_to_target(dst: str) -> Optional[str]:
    """
    :param dst: destination IP address string without port. E.G. '192.168.1.1.'
    :return: IP address string of an interface that can connect to the target. E.G. '192.168.1.4.'
    """
    if sys.platform == "win32":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((dst, 1))
            ip_to_dst = s.getsockname()[0]
        except KeyError:
            logger.debug(
                "Couldn't get an interface to the target, presuming that target is localhost."
            )
            ip_to_dst = "127.0.0.1"
        finally:
            s.close()
        return ip_to_dst
    else:
        # based on scapy implementation

        def atol(x):
            ip = socket.inet_aton(x)
            return struct.unpack("!I", ip)[0]

        routes = get_routes()
        dst = atol(dst)
        paths = []
        for d, m, gw, i, a in routes:
            aa = atol(a)
            if aa == dst:
                paths.append((0xFFFFFFFF, ("lo", a, "0.0.0.0")))
            if (dst & m) == (d & m):
                paths.append((m, (i, a, gw)))
        if not paths:
            return None
        paths.sort()
        ret = paths[-1][1]
        return ret[1]
