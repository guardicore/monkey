import socket
import sys

import array

import struct
import ipaddress
from netifaces import interfaces, ifaddresses, AF_INET

__author__ = 'Barak'


# Local ips function
if sys.platform == "win32":
    def local_ips():
        local_hostname = socket.gethostname()
        return socket.gethostbyname_ex(local_hostname)[2]
else:
    import fcntl

    def local_ips():
        result = []
        try:
            is_64bits = sys.maxsize > 2 ** 32
            struct_size = 40 if is_64bits else 32
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            max_possible = 8  # initial value
            while True:
                struct_bytes = max_possible * struct_size
                names = array.array('B', '\0' * struct_bytes)
                outbytes = struct.unpack('iL', fcntl.ioctl(
                    s.fileno(),
                    0x8912,  # SIOCGIFCONF
                    struct.pack('iL', struct_bytes, names.buffer_info()[0])
                ))[0]
                if outbytes == struct_bytes:
                    max_possible *= 2
                else:
                    break
            namestr = names.tostring()

            for i in range(0, outbytes, struct_size):
                addr = socket.inet_ntoa(namestr[i + 20:i + 24])
                if not addr.startswith('127'):
                    result.append(addr)
                    # name of interface is (namestr[i:i+16].split('\0', 1)[0]
        finally:
            return result
# End of local ips function


def local_ip_addresses():
    ip_list = []
    for interface in interfaces():
        addresses = ifaddresses(interface).get(AF_INET, [])
        ip_list.extend([link['addr'] for link in addresses if link['addr'] != '127.0.0.1'])
    return ip_list


def get_subnets():
    subnets = []
    for interface in interfaces():
        addresses = ifaddresses(interface).get(AF_INET, [])
        subnets.extend([ipaddress.ip_interface(link['addr'] + '/' + link['netmask']).network for link in addresses if link['addr'] != '127.0.0.1'])
    return subnets
