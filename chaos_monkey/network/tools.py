import socket
import select
import logging
import struct

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
    return struct_unpack_tracker(data,index,fmt)


def check_port_tcp(ip, port, timeout=DEFAULT_TIMEOUT, get_banner=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((ip, port))
    except socket.timeout:
        return False, None
    except socket.error, exc:
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


def check_port_udp(ip, port, timeout=DEFAULT_TIMEOUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    
    data = None
    is_open = False
    
    try:
        sock.sendto("-", (ip, port))
        data, _ = sock.recvfrom(BANNER_READ)
        is_open = True
    except:
        pass
    sock.close()

    return is_open, data
