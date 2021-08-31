import logging
import select
import socket
import struct
import sys
import time

from common.network.network_utils import get_host_from_network_location
from infection_monkey.config import WormConfiguration
from infection_monkey.network.info import get_routes, local_ips

DEFAULT_TIMEOUT = 10
BANNER_READ = 1024

logger = logging.getLogger(__name__)
SLEEP_BETWEEN_POLL = 0.5


def struct_unpack_tracker(data, index, fmt):
    """
    Unpacks a struct from the specified index according to specified format.
    Returns the data and the next index
    :param data:  Buffer
    :param index: Position index
    :param fmt: Struct format
    :return: (Data, new index)
    """
    unpacked = struct.unpack_from(fmt, data, index)
    return unpacked, struct.calcsize(fmt)


def struct_unpack_tracker_string(data, index):
    """
    Unpacks a null terminated string from the specified index
    Returns the data and the next index
    :param data:  Buffer
    :param index: Position index
    :return: (Data, new index)
    """
    ascii_len = data[index:].find(b"\0")
    fmt = "%ds" % ascii_len
    return struct_unpack_tracker(data, index, fmt)


def check_tcp_port(ip, port, timeout=DEFAULT_TIMEOUT, get_banner=False):
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
        sock.connect((ip, port))
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


def check_tcp_ports(ip, ports, timeout=DEFAULT_TIMEOUT, get_banner=False):
    """
    Checks whether any of the given ports are open on a target IP.
    :param ip:  IP of host to attack
    :param ports: List of ports to attack. Must not be empty.
    :param timeout: Amount of time to wait for connection
    :param get_banner: T/F if to get first packets from server
    :return: list of open ports. If get_banner=True, then a matching list of banners.
    """
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(len(ports))]
    [s.setblocking(False) for s in sockets]
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
            if err == 10035:  # WSAEWOULDBLOCK is valid, see
                # https://msdn.microsoft.com/en-us/library/windows/desktop/ms740668%28v=vs.85%29
                # .aspx?f=255&MSPPError=-2147217396
                possible_ports.append((port, sock))
                continue
            if err == 115:  # EINPROGRESS     115     /* Operation now in progress */
                possible_ports.append((port, sock))
                continue
            logger.warning("Failed to connect to port %s, error code is %d", port, err)

        if len(possible_ports) != 0:
            timeout = int(round(timeout))  # clamp to integer, to avoid checking input
            sockets_to_try = possible_ports[:]
            connected_ports_sockets = []
            while (timeout >= 0) and sockets_to_try:
                sock_objects = [s[1] for s in sockets_to_try]

                _, writeable_sockets, _ = select.select(sock_objects, sock_objects, sock_objects, 0)
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
            if get_banner and (len(connected_ports_sockets) != 0):
                readable_sockets, _, _ = select.select(
                    [s[1] for s in connected_ports_sockets], [], [], 0
                )
                # read first BANNER_READ bytes. We ignore errors because service might not send a
                # decodable byte string.
                banners = [
                    sock.recv(BANNER_READ).decode(errors="ignore")
                    if sock in readable_sockets
                    else ""
                    for port, sock in connected_ports_sockets
                ]
                pass
            # try to cleanup
            [s[1].close() for s in possible_ports]
            return [port for port, sock in connected_ports_sockets], banners
        else:
            return [], []

    except socket.error as exc:
        logger.warning("Exception when checking ports on host %s, Exception: %s", str(ip), exc)
        return [], []


def tcp_port_to_service(port):
    return "tcp-" + str(port)


def get_interface_to_target(dst):
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


def is_running_on_island():
    current_server_without_port = get_host_from_network_location(WormConfiguration.current_server)
    running_on_island = is_running_on_server(current_server_without_port)
    return running_on_island and WormConfiguration.depth == WormConfiguration.max_depth


def is_running_on_server(ip: str) -> bool:
    return ip in local_ips()
