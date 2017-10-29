import logging
import select
import socket
import struct
import time

DEFAULT_TIMEOUT = 10
BANNER_READ = 1024

LOG = logging.getLogger(__name__)


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
    ascii_len = data[index:].find('\0')
    fmt = "%ds" % ascii_len
    return struct_unpack_tracker(data, index, fmt)


def check_tcp_port(ip, port, timeout=DEFAULT_TIMEOUT, get_banner=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((ip, port))
    except socket.timeout:
        return False, None
    except socket.error as exc:
        LOG.debug("Check port: %s:%s, Exception: %s", ip, port, exc)
        return False, None

    banner = None

    try:
        if get_banner:
            read_ready, _, _ = select.select([sock], [], [], timeout)
            if len(read_ready) > 0:
                banner = sock.recv(BANNER_READ)
    except:
        pass

    sock.close()
    return True, banner


def check_tcp_ports(ip, ports, timeout=DEFAULT_TIMEOUT):
    """
    Checks whether any of the given ports are open on a target IP.
    :param ip:  IP of host to attack
    :param ports: List of ports to attack. Must not be empty.
    :param timeout: Amount of time to wait for connection
    :return: Tuple, T/F on if any port was open and list of open ports
    """
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(len(ports))]
    [s.setblocking(0) for s in sockets]
    good_ports = []
    try:
        for sock, port in zip(sockets, ports):
            LOG.debug("Connecting to port %d" % port)
            err = sock.connect_ex((ip, port))
            if err == 0:
                good_ports.append((port, sock))
            if err == 10035:  # WSAEWOULDBLOCK is valid, see https://msdn.microsoft.com/en-us/library/windows/desktop/ms740668%28v=vs.85%29.aspx?f=255&MSPPError=-2147217396
                good_ports.append((port, sock))

        if len(good_ports) != 0:
            time.sleep(timeout)
            _, connected_sockets, errored_sockets = \
                select.select(
                    [],
                    [s[1] for s in good_ports],
                    [s[1] for s in good_ports],
                    timeout)
            final_ports = [x[0] for x in good_ports if x[1] in connected_sockets]
            LOG.debug(
                "On host %s discovered the following ports %s" % (str(ip), ",".join([str(x) for x in final_ports])))
            # try to cleanup
            [s[1].close() for s in good_ports]
            return True, final_ports
        else:
            return False, None

    except socket.error as exc:
        LOG.warning("Exception when checking ports on host %s, Exception: %s", str(ip), exc)
        return False, None


def check_udp_port(ip, port, timeout=DEFAULT_TIMEOUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    data = None
    is_open = False

    try:
        sock.sendto("-", (ip, port))
        data, _ = sock.recvfrom(BANNER_READ)
        is_open = True
    except socket.error:
        pass
    sock.close()

    return is_open, data
