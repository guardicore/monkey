import socket
import struct
import logging
from threading import Thread
from network.info import local_ips, get_free_tcp_port
from network.firewall import app as firewall
from difflib import get_close_matches
from network.tools import check_port_tcp
import time

__author__ = 'hoffer'

LOG = logging.getLogger(__name__)

MCAST_GROUP = '224.1.1.1'
MCAST_PORT = 5007
BUFFER_READ = 1024
DEFAULT_TIMEOUT = 10
QUIT_TIMEOUT = 1200 #20 minutes

def _set_multicast_socket(timeout=DEFAULT_TIMEOUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    sock.setsockopt(socket.IPPROTO_IP, 
                          socket.IP_ADD_MEMBERSHIP, 
                          struct.pack("4sl", socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY))
    return sock


def find_tunnel(attempts=3, timeout=DEFAULT_TIMEOUT):
    sock = _set_multicast_socket(timeout)

    l_ips = local_ips()

    for attempt in range(0, attempts):
        try:
            sock.sendto("?", (MCAST_GROUP, MCAST_PORT))
            answer, address = sock.recvfrom(BUFFER_READ)

            while answer in ['?', '+', '-']:
                answer, address = sock.recvfrom(BUFFER_READ)

            if answer.find(':') != -1:
                address, port = answer.split(':', 1)
                if address in l_ips:
                    continue
                if not check_port_tcp(address, int(port)):
                    continue

                sock.sendto("+", (address, MCAST_PORT))
                sock.close()
                return (address, port)
        except:
            continue

    return None

def quit_tunnel(address, timeout=DEFAULT_TIMEOUT):
    try:
        sock = _set_multicast_socket(timeout)
        sock.sendto("-", (address, MCAST_PORT))
        sock.close()
        LOG.debug("Success quitting tunnel")        
    except Exception, exc:
        LOG.debug("Exception quitting tunnel: %s", exc)
        return


class MonkeyTunnel(Thread):
    def __init__(self, proxy_class, target_addr=None, target_port=None, timeout=DEFAULT_TIMEOUT):
        self._target_addr = target_addr
        self._target_port = target_port
        self._proxy_class = proxy_class
        self._broad_sock = None
        self._timeout = timeout
        self._stopped = False
        self._clients = []
        super(MonkeyTunnel, self).__init__()

    def run(self):
        self._broad_sock = _set_multicast_socket(self._timeout)

        l_ips = local_ips()

        local_port = get_free_tcp_port()

        if not local_port:
            return

        if not firewall.listen_allowed(localport=local_port):
            LOG.info("Machine firewalled, listen not allowed, not running tunnel.")
            return

        proxy = self._proxy_class(local_port=local_port, dest_host=self._target_addr, dest_port=self._target_port)
        LOG.info("Running tunnel using proxy class: %s, on port %s", proxy.__class__.__name__, local_port)
        proxy.start()

        while not self._stopped:
            try:
                search, address = self._broad_sock.recvfrom(BUFFER_READ)
                if '?' == search:
                    ip_match = get_close_matches(address[0], l_ips) or l_ips
                    if ip_match:
                        answer = '%s:%d' % (ip_match[0], local_port)
                        LOG.debug("Got tunnel request from %s, answering with %s", address[0], answer)
                        self._broad_sock.sendto(answer, (MCAST_GROUP, MCAST_PORT))
                elif '+' == search:
                    if not address[0] in self._clients:
                        self._clients.append(address[0])
                elif '-' == search:
                        self._clients = [client for client in self._clients if client != address[0]]
            
            except socket.timeout:
                continue

        LOG.info("Stopping tunnel, waiting for clients")
        stop_time = time.time()
        while self._clients and (time.time() - stop_time < QUIT_TIMEOUT):
            try:
                search, address = self._broad_sock.recvfrom(BUFFER_READ)
                if '-' == search:
                    self._clients = [client for client in self._clients if client != address[0]]
            except socket.timeout:
                continue
        LOG.info("Closing tunnel")
        self._broad_sock.close()
        proxy.stop()
        proxy.join()

    def stop(self):
        self._stopped = True