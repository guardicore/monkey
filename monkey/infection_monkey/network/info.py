import abc
import socket
import struct
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from monkeytoolbox import get_os
from monkeytypes import NetworkPort, OperatingSystem

if get_os() == OperatingSystem.LINUX:
    from fcntl import ioctl


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


def get_routes() -> List[Tuple[int, int, str, bytes, str]]:
    if get_os() == OperatingSystem.WINDOWS:
        raise NotImplementedError()

    routes = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for line in _read_route_file():
        dst: bytes
        msk: bytes
        iff, dst, gw, flags, msk = _extract_network_info(line)
        if flags & RTF_UP == 0:
            continue
        if flags & RTF_REJECT:
            continue
        ifaddr: Optional[str] = _get_interface_address(s, iff)
        if ifaddr is None:
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

    ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", LOOPBACK_NAME))
    addrfamily = struct.unpack("h", ifreq[16:18])[0]
    if addrfamily == socket.AF_INET:
        ifreq2 = ioctl(s, SIOCGIFNETMASK, struct.pack("16s16x", LOOPBACK_NAME))
        mask = socket.ntohl(struct.unpack("I", ifreq2[20:24])[0])
        destination = socket.ntohl(struct.unpack("I", ifreq[20:24])[0]) & mask
        ifaddress = socket.inet_ntoa(ifreq[20:24])
        routes.append((destination, mask, "0.0.0.0", LOOPBACK_NAME, ifaddress))

    return routes


def _read_route_file() -> List[str]:
    try:
        with open("/proc/net/route", "r") as f:
            return f.readlines()[1:]
    except IOError:
        return []


def _extract_network_info(line: str) -> Tuple[bytes, bytes, bytes, int, bytes]:
    values = [var.encode() for var in line.split()]
    iff: bytes = values[0]
    dst: bytes = values[1]
    gw: bytes = values[2]
    flags: int = int(values[3], 16)
    msk: bytes = values[7]
    return iff, dst, gw, flags, msk


def _get_interface_address(s: socket.socket, iff: bytes) -> Optional[str]:
    try:
        ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", iff))
    except IOError:
        return "0.0.0.0"
    addrfamily = struct.unpack("h", ifreq[16:18])[0]
    if addrfamily == socket.AF_INET:
        return socket.inet_ntoa(ifreq[20:24])
    return None


class ITCPPortSelector(metaclass=abc.ABCMeta):
    """
    An interface for components to select an available TCP port
    that a new server can listen on.
    """

    @abc.abstractmethod
    def get_free_tcp_port(
        self,
        min_range: int = 1024,
        max_range: int = 65535,
        lease_time_sec: float = 30,
        preferred_ports: Sequence[NetworkPort] = [],
    ) -> Optional[NetworkPort]:
        """
        Get a free TCP port that a new server can listen on

        :param min_range: The smallest port number a random port can be chosen from, defaults to
                          1024
        :param max_range: The largest port number a random port can be chosen from, defaults to
                          65535
        :param lease_time_sec: The amount of time a port should be reserved for if the OS does not
                               report it as in use, defaults to 30 seconds
        :param preferred_ports: A sequence of ports that should be tried first
        :return: The selected port, or None if no ports are available
        """
