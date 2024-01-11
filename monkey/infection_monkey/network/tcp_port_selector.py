import threading
from itertools import chain
from random import shuffle  # noqa: DUO102
from typing import Dict, Iterable, Iterator, Optional, Sequence, Set

import psutil
from egg_timer import EggTimer
from monkeytypes import IntRange, NetworkPort

from .info import ITCPPortSelector
from .ports import COMMON_PORTS


def port_range(int_range: IntRange) -> Iterator[NetworkPort]:
    """Yields port values in the provided range, bounded by [0, 65535]."""
    min_ = max(0, int_range.min)
    max_ = min(65535, int_range.max) + 1
    return map(NetworkPort, range(min_, max_))


class TCPPortSelector(ITCPPortSelector):
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

    def __init__(self):
        self._leases: Dict[NetworkPort, EggTimer] = {}
        self._lock = threading.Lock()

    def get_free_tcp_port(
        self,
        min_range: int = 1024,
        max_range: int = 65535,
        lease_time_sec: float = 30,
        preferred_ports: Sequence[NetworkPort] = [],
    ) -> Optional[NetworkPort]:
        """
        Get a free TCP port that a new server can listen on

        This function will first check if any of the preferred ports are available. If not, it will
        attempt to provide a well-known port that the caller can listen on. If no well-known ports
        are available, a random port will be selected.

        :param min_range: The smallest port number a random port can be chosen from, defaults to
                          1024
        :param max_range: The largest port number a random port can be chosen from, defaults to
                          65535
        :param lease_time_sec: The amount of time a port should be reserved for if the OS does not
                               report it as in use, defaults to 30 seconds
        :param preferred_ports: A sequence of ports that should be tried first
        :return: The selected port, or None if no ports are available
        """
        with self._lock:
            ports_in_use = {
                NetworkPort(conn.laddr[1]) for conn in psutil.net_connections()  # type: ignore
            }

            port = self._get_first_free_port(
                ports_in_use, chain(preferred_ports, COMMON_PORTS), lease_time_sec
            )
            if port is not None:
                return port

            return self._get_free_random_port(ports_in_use, min_range, max_range, lease_time_sec)

    def _get_first_free_port(
        self,
        ports_in_use: Set[NetworkPort],
        ports_to_check: Iterable[NetworkPort],
        lease_time_sec: float,
    ) -> Optional[NetworkPort]:
        for port in ports_to_check:
            if self._port_is_available(port, ports_in_use):
                self._reserve_port(port, lease_time_sec)
                return port

        return None

    def _get_free_random_port(
        self, ports_in_use: Set[NetworkPort], min_range: int, max_range: int, lease_time_sec: float
    ) -> Optional[NetworkPort]:
        ports = list(port_range(IntRange(min_range, max_range)))
        shuffle(ports)
        for port in ports:
            if self._port_is_available(port, ports_in_use):
                self._reserve_port(port, lease_time_sec)
                return port

        return None

    def _port_is_available(self, port: NetworkPort, ports_in_use: Set[NetworkPort]) -> bool:
        if port in ports_in_use:
            return False

        if port not in self._leases:
            return True

        if self._leases[port].is_expired():
            return True

        return False

    def _reserve_port(self, port: NetworkPort, lease_time_sec: float):
        timer = EggTimer()
        timer.set(lease_time_sec)
        self._leases[port] = timer
