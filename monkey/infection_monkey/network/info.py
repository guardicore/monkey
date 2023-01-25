import socket
import struct
from dataclasses import dataclass
from multiprocessing.context import BaseContext
from multiprocessing.managers import DictProxy, SyncManager
from random import shuffle  # noqa: DUO102
from typing import Optional, Set

import psutil
from egg_timer import EggTimer

from common.utils.environment import is_windows_os

from .ports import COMMON_PORTS

# Timeout for monkey connections
LOOPBACK_NAME = b"lo"
SIOCGIFADDR = 0x8915  # get PA address
SIOCGIFNETMASK = 0x891B  # get network PA mask
RTF_UP = 0x0001  # Route usable
RTF_REJECT = 0x0200


@dataclass
class NetworkAddress:
    ip: str
    domain: Optional[str]


if is_windows_os():

    def get_routes():
        raise NotImplementedError()

else:
    from fcntl import ioctl

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


class TCPPortSelector:
    """
    Select an available TCP port that a new server can listen on

    Examines the system to find which ports are not in use and makes an intelligent decision
    regarding what port can be used to host a server. In multithreaded applications, a race occurs
    between the time when the OS reports that a port is free and when the port is actually used. In
    other words, two threads which request a free port simultaneously may be handed the same port,
    as the OS will report that the port is not in use. To combat this, the TCPPortSelector will
    reserve a port for a period of time to give the requester ample time to start their server. Once
    the requester's server is listening on the port, the OS will report the port as "LISTEN".
    """

    def __init__(self, context: BaseContext, manager: SyncManager):
        self._leases: DictProxy[int, EggTimer] = manager.dict()
        self._lock = context.Lock()

    def get_free_tcp_port(
        self, min_range: int = 1024, max_range: int = 65535, lease_time_sec: float = 30
    ) -> Optional[int]:
        """
        Get a free TCP port that a new server can listen on

        This function will attempt to provide a well-known port that the caller can listen on. If no
        well-known ports are available, a random port will be selected.

        :param min_range: The smallest port number a random port can be chosen from, defaults to
                          1024
        :param max_range: The largest port number a random port can be chosen from, defaults to
                          65535
        :param lease_time_sec: The amount of time a port should be reserved for if the OS does not
                               report it as in use, defaults to 30 seconds
        """
        with self._lock:
            ports_in_use = {conn.laddr[1] for conn in psutil.net_connections()}

            common_port = self._get_free_common_port(ports_in_use, lease_time_sec)
            if common_port is not None:
                return common_port

            return self._get_free_random_port(ports_in_use, min_range, max_range, lease_time_sec)

    def _get_free_common_port(self, ports_in_use: Set[int], lease_time_sec: float) -> Optional[int]:
        for port in COMMON_PORTS:
            if self._port_is_available(port, ports_in_use):
                self._reserve_port(port, lease_time_sec)
                return port

        return None

    def _get_free_random_port(
        self, ports_in_use: Set[int], min_range: int, max_range: int, lease_time_sec: float
    ) -> Optional[int]:
        min_range = max(1, min_range)
        # In range the first argument will be in the list and the second one won't.
        # which means that if we select 65535 as max range, that port will not get
        # into the range
        max_range = min(65535, max_range) + 1
        ports = list(range(min_range, max_range))
        shuffle(ports)
        for port in ports:
            if self._port_is_available(port, ports_in_use):
                self._reserve_port(port, lease_time_sec)
                return port

        return None

    def _port_is_available(self, port: int, ports_in_use: Set[int]) -> bool:
        if port in ports_in_use:
            return False

        if port not in self._leases:
            return True

        if self._leases[port].is_expired():
            return True

        return False

    def _reserve_port(self, port: int, lease_time_sec: float):
        timer = EggTimer()
        timer.set(lease_time_sec)
        self._leases[port] = timer


# TODO: This function is here because existing components rely on it. Refactor these components to
#       accept a TCPPortSelector instance and use that instead.
def get_free_tcp_port(min_range=1024, max_range=65535, lease_time_sec=30):
    return get_free_tcp_port.port_selector.get_free_tcp_port(min_range, max_range, lease_time_sec)


get_free_tcp_port.port_selector = TCPPortSelector()  # type: ignore[attr-defined]
