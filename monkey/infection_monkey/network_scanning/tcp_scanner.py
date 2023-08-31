import logging
import select
import socket
from ipaddress import IPv4Address
from pprint import pformat
from time import sleep, time
from typing import Collection, Dict, Iterable, Mapping, Tuple

from egg_timer import EggTimer

from common.agent_events import TCPScanEvent
from common.event_queue import IAgentEventQueue
from common.types import AgentID, NetworkPort, PortStatus
from infection_monkey.i_puppet import PortScanData, PortScanDataDict
from infection_monkey.network.tools import BANNER_READ, DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)

POLL_INTERVAL = 0.5
EMPTY_PORT_SCAN = PortScanDataDict()


def scan_tcp_ports(
    host: str,
    ports_to_scan: Collection[NetworkPort],
    timeout: float,
    agent_event_queue: IAgentEventQueue,
    agent_id: AgentID,
) -> PortScanDataDict:
    try:
        return _scan_tcp_ports(host, ports_to_scan, timeout, agent_event_queue, agent_id)
    except Exception:
        logger.exception("Unhandled exception occurred while trying to scan tcp ports")
        return EMPTY_PORT_SCAN


def _scan_tcp_ports(
    host: str,
    ports_to_scan: Collection[NetworkPort],
    timeout: float,
    agent_event_queue: IAgentEventQueue,
    agent_id: AgentID,
) -> PortScanDataDict:
    event_timestamp, open_ports = _check_tcp_ports(host, ports_to_scan, timeout)

    port_scan_data = _build_port_scan_data(ports_to_scan, open_ports)

    tcp_scan_event = _generate_tcp_scan_event(host, port_scan_data, event_timestamp, agent_id)
    agent_event_queue.publish(tcp_scan_event)

    return port_scan_data


def _generate_tcp_scan_event(
    host: str,
    port_scan_data_dict: PortScanDataDict,
    event_timestamp: float,
    agent_id: AgentID,
):
    port_statuses = {port: psd.status for port, psd in port_scan_data_dict.items()}

    # TODO: Tag with the appropriate MITRE ATT&CK tags
    return TCPScanEvent(
        source=agent_id,
        target=IPv4Address(host),
        timestamp=event_timestamp,
        ports=port_statuses,
    )


def _build_port_scan_data(
    ports_to_scan: Iterable[NetworkPort], open_ports: Mapping[NetworkPort, str]
) -> PortScanDataDict:
    port_scan_data = PortScanDataDict()
    for port in ports_to_scan:
        if port in open_ports:
            banner = open_ports[port]

            port_scan_data[port] = PortScanData(port=port, status=PortStatus.OPEN, banner=banner)
        else:
            port_scan_data[port] = _get_closed_port_data(port)

    return port_scan_data


def _get_closed_port_data(port: NetworkPort) -> PortScanData:
    return PortScanData(port=port, status=PortStatus.CLOSED)


def _check_tcp_ports(
    ip: str, ports_to_scan: Collection[NetworkPort], timeout: float = DEFAULT_TIMEOUT
) -> Tuple[float, Dict[NetworkPort, str]]:
    """
    Checks whether any of the given ports are open on a target IP.
    :param ip:  IP of host to attack
    :param ports_to_scan: An iterable of ports to scan. Must not be empty.
    :param timeout: Amount of time to wait for connection
    """
    event_timestamp = time()
    open_ports: Dict[NetworkPort, str] = {}

    try:
        ports_sockets = _create_sockets(ports_to_scan)
        possible_ports, connected_ports_sockets = _connect_sockets(ip, ports_sockets)
        logger.debug(
            "Connecting to the following ports %s" % ",".join((str(x) for x in ports_to_scan))
        )

        if possible_ports:
            timer = EggTimer()
            timer.set(timeout)

            _process_connected_sockets(connected_ports_sockets, possible_ports, open_ports, timer)

        logger.info(
            f"Discovered the following ports on {ip}: "
            f"{pformat([port for port, _ in connected_ports_sockets])}"
        )

    except socket.error as exc:
        logger.warning("Exception when checking ports on host %s, Exception: %s", str(ip), exc)

    _clean_up_sockets(possible_ports, connected_ports_sockets)

    return event_timestamp, open_ports


def _create_sockets(ports: Collection[NetworkPort]) -> Dict[NetworkPort, socket.socket]:
    ports_sockets = {}
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        ports_sockets[port] = sock
    return ports_sockets


def _connect_sockets(ip: str, ports_sockets: Dict[NetworkPort, socket.socket]) -> Tuple[set, set]:
    possible_ports_sockets = set()
    connected_ports_sockets = set()

    for port, sock in ports_sockets.items():
        err = sock.connect_ex((ip, port))
        if err == 0:  # immediate connect
            connected_ports_sockets.add((port, sock))
            possible_ports_sockets.add((port, sock))
        elif err == 10035:  # WSAEWOULDBLOCK is valid.
            # https://docs.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-connect
            # says, "Use the select function to determine the completion of the connection
            # request by checking to see if the socket is writable," which is being done below.
            possible_ports_sockets.add((port, sock))
        elif err == 115:  # EINPROGRESS     115     /* Operation now in progress */
            possible_ports_sockets.add((port, sock))
        else:
            logger.warning("Failed to connect to port %s, error code is %d", port, err)

    return possible_ports_sockets, connected_ports_sockets


def _process_connected_sockets(
    connected_ports_sockets: set,
    possible_ports_sockets: set,
    open_ports: Dict[NetworkPort, str],
    timer: EggTimer,
):
    ports_sockets_to_try = possible_ports_sockets.copy()

    while not timer.is_expired() and ports_sockets_to_try:
        sleep(min(POLL_INTERVAL, timer.time_remaining_sec))

        sock_objects = [s[1] for s in ports_sockets_to_try]

        _, writeable_sockets, _ = select.select([], sock_objects, [], timer.time_remaining_sec)
        for s in writeable_sockets:
            try:
                connected_ports_sockets.add((s.getpeername()[1], s))
            except socket.error:
                pass

        ports_sockets_to_try = ports_sockets_to_try - connected_ports_sockets

    open_ports.update({port: "" for port, _ in connected_ports_sockets})

    if connected_ports_sockets:
        readable_sockets, _, _ = select.select(
            [s[1] for s in connected_ports_sockets], [], [], timer.time_remaining_sec
        )
        for port, sock in connected_ports_sockets:
            if sock in readable_sockets:
                open_ports[port] = sock.recv(BANNER_READ).decode(errors="ignore")
            else:
                open_ports[port] = ""


def _clean_up_sockets(
    possible_ports_sockets: Iterable[Tuple[NetworkPort, socket.socket]],
    connected_ports_sockets: Iterable[Tuple[NetworkPort, socket.socket]],
):
    # Only call shutdown() on sockets we know to be connected
    for port, s in connected_ports_sockets:
        try:
            s.shutdown(socket.SHUT_RDWR)
        except socket.error as exc:
            logger.warning(f"Error occurred while shutting down socket on port {port}: {exc}")

    # Call close() for all sockets
    for port, s in possible_ports_sockets:
        try:
            s.close()
        except socket.error as exc:
            logger.warning(f"Error occurred while closing socket on port {port}: {exc}")
