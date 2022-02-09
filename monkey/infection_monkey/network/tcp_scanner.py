import logging
import select
import socket
import time
from itertools import zip_longest
from typing import Dict, List, Set

from infection_monkey.i_puppet import PortScanData, PortStatus
from infection_monkey.network.tools import BANNER_READ, DEFAULT_TIMEOUT, tcp_port_to_service

SLEEP_BETWEEN_POLL = 0.5

logger = logging.getLogger(__name__)


def scan_tcp_ports(host: str, ports: List[int], timeout: float) -> Dict[int, PortScanData]:
    ports_scan = {}

    open_ports, banners = _check_tcp_ports(host, ports, timeout)
    open_ports = set(open_ports)

    for port, banner in zip_longest(ports, banners, fillvalue=None):
        ports_scan[port] = _build_port_scan_data(port, open_ports, banner)

    return ports_scan


def _build_port_scan_data(port: int, open_ports: Set[int], banner: str) -> PortScanData:
    if port in open_ports:
        service = tcp_port_to_service(port)
        return PortScanData(port, PortStatus.OPEN, banner, service)
    else:
        return _get_closed_port_data(port)


def _get_closed_port_data(port: int) -> PortScanData:
    return PortScanData(port, PortStatus.CLOSED, None, None)


def _check_tcp_ports(ip: str, ports: List[int], timeout: float = DEFAULT_TIMEOUT):
    """
    Checks whether any of the given ports are open on a target IP.
    :param ip:  IP of host to attack
    :param ports: List of ports to attack. Must not be empty.
    :param timeout: Amount of time to wait for connection
    :return: List of open ports.
    """
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(len(ports))]
    for s in sockets:
        s.setblocking(False)

    possible_ports = []
    connected_ports_sockets = []
    try:
        logger.debug("Connecting to the following ports %s" % ",".join((str(x) for x in ports)))
        for sock, port in zip(sockets, ports):
            err = sock.connect_ex((ip, port))
            if err == 0:  # immediate connect
                connected_ports_sockets.append((port, sock))
                possible_ports.append((port, sock))
                continue
            if err == 10035:  # WSAEWOULDBLOCK is valid.
                # https://docs.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-connect
                # says, "Use the select function to determine the completion of the connection
                # request by checking to see if the socket is writable," which is being done below.
                possible_ports.append((port, sock))
                continue
            if err == 115:  # EINPROGRESS     115     /* Operation now in progress */
                possible_ports.append((port, sock))
                continue
            logger.warning("Failed to connect to port %s, error code is %d", port, err)

        if len(possible_ports) != 0:
            timeout = int(round(timeout))  # clamp to integer, to avoid checking input
            sockets_to_try = possible_ports.copy()
            while (timeout >= 0) and sockets_to_try:
                sock_objects = [s[1] for s in sockets_to_try]

                _, writeable_sockets, _ = select.select([], sock_objects, [], 0)
                for s in writeable_sockets:
                    try:  # actual test
                        connected_ports_sockets.append((s.getpeername()[1], s))
                    except socket.error:  # bad socket, select didn't filter it properly
                        pass
                sockets_to_try = [s for s in sockets_to_try if s not in connected_ports_sockets]
                if sockets_to_try:
                    time.sleep(SLEEP_BETWEEN_POLL)
                    timeout -= SLEEP_BETWEEN_POLL

            logger.debug(
                "On host %s discovered the following ports %s"
                % (str(ip), ",".join([str(s[0]) for s in connected_ports_sockets]))
            )

            banners = []
            if len(connected_ports_sockets) != 0:
                readable_sockets, _, _ = select.select(
                    [s[1] for s in connected_ports_sockets], [], [], 0
                )
                # read first BANNER_READ bytes. We ignore errors because service might not send a
                # decodable byte string.
                for port, sock in connected_ports_sockets:
                    if sock in readable_sockets:
                        banners.append(sock.recv(BANNER_READ).decode(errors="ignore"))
                    else:
                        banners.append("")

            # try to cleanup
            for s in possible_ports:
                s[1].shutdown(socket.SHUT_RDWR)
                s[1].close()

            # TODO: Rework the return of this function. Consider using dictionary
            return [port for port, sock in connected_ports_sockets], banners
        else:
            return [], []

    except socket.error as exc:
        logger.warning("Exception when checking ports on host %s, Exception: %s", str(ip), exc)
        return [], []
