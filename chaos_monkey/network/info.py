import os
import sys
import array
import socket
import struct
import psutil
import ipaddress
from subprocess import check_output
from random import randint

if sys.platform == "win32":
    import netifaces


    def local_ips():
        local_hostname = socket.gethostname()
        return socket.gethostbyname_ex(local_hostname)[2]


    def get_host_subnets(only_ips=False):
        network_adapters = []
        valid_ips = local_ips()
        if only_ips:
            return valid_ips
        interfaces = [netifaces.ifaddresses(x) for x in netifaces.interfaces()]
        for inte in interfaces:
            if netifaces.AF_INET in inte:
                for add in inte[netifaces.AF_INET]:
                    if "netmask" in add and add["addr"] in valid_ips:
                        network_adapters.append((add["addr"], add["netmask"]))
        return network_adapters

else:
    import fcntl


    def get_host_subnets(only_ips=False):
        """Get the list of Linux network adapters."""
        max_bytes = 8096
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            offset1 = 16
            offset2 = 40
        else:
            offset1 = 32
            offset2 = 32
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', '\0' * max_bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            sock.fileno(),
            0x8912,
            struct.pack('iL', max_bytes, names.buffer_info()[0])))[0]
        adapter_names = [names.tostring()[n_cnt:n_cnt + offset1].split('\0', 1)[0]
                         for n_cnt in xrange(0, outbytes, offset2)]
        network_adapters = []
        for adapter_name in adapter_names:
            ip_address = socket.inet_ntoa(fcntl.ioctl(
                sock.fileno(),
                0x8915,
                struct.pack('256s', adapter_name))[20:24])
            if ip_address.startswith('127'):
                continue
            subnet_mask = socket.inet_ntoa(fcntl.ioctl(
                sock.fileno(),
                0x891b,
                struct.pack('256s', adapter_name))[20:24])

            if only_ips:
                network_adapters.append(ip_address)
            else:
                network_adapters.append((ip_address, subnet_mask))

        return network_adapters


    def local_ips():
        return get_host_subnets(only_ips=True)


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


def get_ips_from_interfaces():
    res = []
    ifs = get_host_subnets()
    for interface in ifs:
        ipint = ipaddress.ip_interface(u"%s/%s" % interface)
        # limit subnet scans to class C only
        if ipint.network.num_addresses > 255:
            ipint = ipaddress.ip_interface(u"%s/24" % interface[0])
        for addr in ipint.network.hosts():
            if str(addr) == interface[0]:
                continue
            res.append(str(addr))
    return res

if sys.platform == "win32":
    def get_ip_for_connection(target_ip):
        return None
else:
    def get_ip_for_connection(target_ip):
        try:
            query_str = 'ip route get %s' % target_ip
            resp = check_output(query_str.split())
            substr = resp.split()
            src = substr[substr.index('src')+1]
            return src
        except Exception:
            return None