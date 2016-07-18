import os
import sys
import socket
import struct
import array
from random import randint

__author__ = 'hoffer'

if sys.platform == "win32":
    def local_ips():
        local_hostname = socket.gethostname()
        return socket.gethostbyname_ex(local_hostname)[2]

else:
    import fcntl    

    def local_ips():
        result = []
        try:
            is_64bits = sys.maxsize > 2**32
            struct_size = 40 if is_64bits else 32
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            max_possible = 8 # initial value
            while True:
                bytes = max_possible * struct_size
                names = array.array('B', '\0' * bytes)
                outbytes = struct.unpack('iL', fcntl.ioctl(
                    s.fileno(),
                    0x8912,  # SIOCGIFCONF
                    struct.pack('iL', bytes, names.buffer_info()[0])
                ))[0]
                if outbytes == bytes:
                    max_possible *= 2
                else:
                    break
            namestr = names.tostring()

            for i in range(0, outbytes, struct_size):
                addr = socket.inet_ntoa(namestr[i+20:i+24])
                if not addr.startswith('127'):
                    result.append(addr)
                    # name of interface is (namestr[i:i+16].split('\0', 1)[0]
        finally:
            return result


def get_free_tcp_port(min_range=1000, max_range=65535):
    start_range = min(1, min_range)
    max_range = min(65535, max_range)
    
    in_use = [conn.laddr[1] for conn in psutil.net_connections()]

    for i in range(min_range, max_range):
        port = randint(start_range, max_range)
        
        if port not in in_use:
            return port

    return None

def check_internet_access(services):
    ping_str = "-n 1" if sys.platform.startswith("win") else "-c 1"
    for host in services:
        if os.system("ping " + ping_str + " " + host) == 0:
            return True
    return False
