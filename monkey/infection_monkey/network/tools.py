import logging
import sys
import subprocess
import select
import socket
import struct
import time

from six import text_type
import ipaddress

DEFAULT_TIMEOUT = 10
BANNER_READ = 1024

LOG = logging.getLogger(__name__)
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
    ascii_len = data[index:].find('\0')
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
        LOG.debug("Check port: %s:%s, Exception: %s", ip, port, exc)
        return False, None

    banner = None

    try:
        if get_banner:
            read_ready, _, _ = select.select([sock], [], [], timeout)
            if len(read_ready) > 0:
                banner = sock.recv(BANNER_READ)
    except socket.error:
        pass

    sock.close()
    return True, banner


def check_udp_port(ip, port, timeout=DEFAULT_TIMEOUT):
    """
    Checks if a given UDP port is open by checking if it replies to an empty message
    :param ip:  Target IP
    :param port: Target port
    :param timeout: Timeout to wait
    :return: Tuple, T/F + banner
    """
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
    [s.setblocking(0) for s in sockets]
    possible_ports = []
    connected_ports_sockets = []
    try:
        LOG.debug("Connecting to the following ports %s" % ",".join((str(x) for x in ports)))
        for sock, port in zip(sockets, ports):
            err = sock.connect_ex((ip, port))
            if err == 0:  # immediate connect
                connected_ports_sockets.append((port, sock))
                possible_ports.append((port, sock))
                continue
            if err == 10035:  # WSAEWOULDBLOCK is valid, see
                # https://msdn.microsoft.com/en-us/library/windows/desktop/ms740668%28v=vs.85%29.aspx?f=255&MSPPError=-2147217396
                possible_ports.append((port, sock))
                continue
            if err == 115:  # EINPROGRESS     115     /* Operation now in progress */
                possible_ports.append((port, sock))
                continue
            LOG.warning("Failed to connect to port %s, error code is %d", port, err)

        if len(possible_ports) != 0:
            timeout = int(round(timeout))  # clamp to integer, to avoid checking input
            sockets_to_try = possible_ports[:]
            connected_ports_sockets = []
            while (timeout >= 0) and len(sockets_to_try):
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

            LOG.debug(
                "On host %s discovered the following ports %s" %
                (str(ip), ",".join([str(s[0]) for s in connected_ports_sockets])))
            banners = []
            if get_banner and (len(connected_ports_sockets) != 0):
                readable_sockets, _, _ = select.select([s[1] for s in connected_ports_sockets], [], [], 0)
                # read first BANNER_READ bytes
                banners = [sock.recv(BANNER_READ) if sock in readable_sockets else ""
                           for port, sock in connected_ports_sockets]
                pass
            # try to cleanup
            [s[1].close() for s in possible_ports]
            return [port for port, sock in connected_ports_sockets], banners
        else:
            return [], []

    except socket.error as exc:
        LOG.warning("Exception when checking ports on host %s, Exception: %s", str(ip), exc)
        return [], []


def tcp_port_to_service(port):
    return 'tcp-' + str(port)


def traceroute(target_ip, ttl):
    """
    Traceroute for a specific IP.
    :param target_ip: Destination
    :param ttl: Max TTL
    :return: Sequence of IPs in the way
    """
    if sys.platform == "win32":
        try:
            # we'll just use tracert because that's always there
            cli = ["tracert",
                   "-d",
                   "-w", "250",
                   "-h", str(ttl),
                   target_ip]
            proc_obj = subprocess.Popen(cli, stdout=subprocess.PIPE)
            stdout, stderr = proc_obj.communicate()
            ip_lines = stdout.split('\r\n')[3:-3]
            trace_list = []
            for line in ip_lines:
                tokens = line.split()
                last_token = tokens[-1]
                try:
                    ip_addr = ipaddress.ip_address(text_type(last_token))
                except ValueError:
                    ip_addr = ""
                trace_list.append(ip_addr)
            return trace_list
        except:
            return []
    else:  # linux based hopefully
        # implementation note: We're currently going to just use ping.
        # reason is, implementing a non root requiring user is complicated (see traceroute(8) code)
        # while this is just ugly
        # we can't use traceroute because it's not always installed
        current_ttl = 1
        trace_list = []
        while current_ttl <= ttl:
            try:
                cli = ["ping",
                       "-c", "1",
                       "-w", "1",
                       "-t", str(current_ttl),
                       target_ip]
                proc_obj = subprocess.Popen(cli, stdout=subprocess.PIPE)
                stdout, stderr = proc_obj.communicate()
                ip_line = stdout.split('\n')
                ip_line = ip_line[1]
                ip = ip_line.split()[1]
                trace_list.append(ipaddress.ip_address(text_type(ip)))
            except (IndexError, ValueError):
                # assume we failed parsing output
                trace_list.append("")
            current_ttl += 1
        return trace_list
