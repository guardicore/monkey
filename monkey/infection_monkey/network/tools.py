import logging
import socket
import struct
import sys
from typing import Optional

from common.common_consts.timeouts import CONNECTION_TIMEOUT
from infection_monkey.network.info import get_routes

DEFAULT_TIMEOUT = CONNECTION_TIMEOUT
BANNER_READ = 1024

logger = logging.getLogger(__name__)


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
