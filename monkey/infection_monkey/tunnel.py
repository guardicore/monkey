import logging
import socket
import struct
import time
from threading import Thread

from infection_monkey.model import VictimHost
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.info import get_free_tcp_port, local_ips
from infection_monkey.network.tools import (check_tcp_port,
                                            get_interface_to_target)
from infection_monkey.transport.base import get_last_serve_time

__author__ = 'hoffer'

LOG = logging.getLogger(__name__)

MCAST_GROUP = '224.1.1.1'
MCAST_PORT = 5007
BUFFER_READ = 1024
DEFAULT_TIMEOUT = 10
QUIT_TIMEOUT = 60 * 10  # 10 minutes


def _set_multicast_socket(timeout=DEFAULT_TIMEOUT, adapter=''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((adapter, MCAST_PORT))
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_ADD_MEMBERSHIP,
                    struct.pack("4sl", socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY))
    return sock


def _check_tunnel(address, port, existing_sock=None):
    if not existing_sock:
        sock = _set_multicast_socket()
    else:
        sock = existing_sock

    LOG.debug("Checking tunnel %s:%s", address, port)
    is_open, _ = check_tcp_port(address, int(port))
    if not is_open:
        LOG.debug("Could not connect to %s:%s", address, port)
        if not existing_sock:
            sock.close()
        return False

    try:
        sock.sendto(b"+", (address, MCAST_PORT))
    except Exception as exc:
        LOG.debug("Caught exception in tunnel registration: %s", exc)

    if not existing_sock:
        sock.close()
    return True


def find_tunnel(default=None, attempts=3, timeout=DEFAULT_TIMEOUT):
    l_ips = local_ips()

    if default:
        if default.find(':') != -1:
            address, port = default.split(':', 1)
            if _check_tunnel(address, port):
                return address, port

    for adapter in l_ips:
        for attempt in range(0, attempts):
            try:
                LOG.info("Trying to find using adapter %s", adapter)
                sock = _set_multicast_socket(timeout, adapter)
                sock.sendto(b"?", (MCAST_GROUP, MCAST_PORT))
                tunnels = []

                while True:
                    try:
                        answer, address = sock.recvfrom(BUFFER_READ)
                        if answer not in [b'?', b'+', b'-']:
                            tunnels.append(answer)
                    except socket.timeout:
                        break

                for tunnel in tunnels:
                    if tunnel.find(':') != -1:
                        address, port = tunnel.split(':', 1)
                        if address in l_ips:
                            continue

                        if _check_tunnel(address, port, sock):
                            sock.close()
                            return address, port

            except Exception as exc:
                LOG.debug("Caught exception in tunnel lookup: %s", exc)
                continue

    return None


def quit_tunnel(address, timeout=DEFAULT_TIMEOUT):
    try:
        sock = _set_multicast_socket(timeout)
        sock.sendto(b"-", (address, MCAST_PORT))
        sock.close()
        LOG.debug("Success quitting tunnel")
    except Exception as exc:
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
        self.local_port = None
        super(MonkeyTunnel, self).__init__()
        self.daemon = True
        self.l_ips = None

    def run(self):
        self._broad_sock = _set_multicast_socket(self._timeout)
        self.l_ips = local_ips()
        self.local_port = get_free_tcp_port()

        if not self.local_port:
            return

        if not firewall.listen_allowed(localport=self.local_port):
            LOG.info("Machine firewalled, listen not allowed, not running tunnel.")
            return

        proxy = self._proxy_class(local_port=self.local_port, dest_host=self._target_addr, dest_port=self._target_port)
        LOG.info("Running tunnel using proxy class: %s, listening on port %s, routing to: %s:%s",
                 proxy.__class__.__name__,
                 self.local_port,
                 self._target_addr,
                 self._target_port)
        proxy.start()

        while not self._stopped:
            try:
                search, address = self._broad_sock.recvfrom(BUFFER_READ)
                if b'?' == search:
                    ip_match = get_interface_to_target(address[0])
                    if ip_match:
                        answer = '%s:%d' % (ip_match, self.local_port)
                        LOG.debug("Got tunnel request from %s, answering with %s", address[0], answer)
                        self._broad_sock.sendto(answer.encode(), (address[0], MCAST_PORT))
                elif b'+' == search:
                    if not address[0] in self._clients:
                        LOG.debug("Tunnel control: Added %s to watchlist", address[0])
                        self._clients.append(address[0])
                elif b'-' == search:
                    LOG.debug("Tunnel control: Removed %s from watchlist", address[0])
                    self._clients = [client for client in self._clients if client != address[0]]

            except socket.timeout:
                continue

        LOG.info("Stopping tunnel, waiting for clients: %s" % repr(self._clients))

        # wait till all of the tunnel clients has been disconnected, or no one used the tunnel in QUIT_TIMEOUT seconds
        while self._clients and (time.time() - get_last_serve_time() < QUIT_TIMEOUT):
            try:
                search, address = self._broad_sock.recvfrom(BUFFER_READ)
                if b'-' == search:
                    LOG.debug("Tunnel control: Removed %s from watchlist", address[0])
                    self._clients = [client for client in self._clients if client != address[0]]
            except socket.timeout:
                continue

        LOG.info("Closing tunnel")
        self._broad_sock.close()
        proxy.stop()
        proxy.join()

    def set_tunnel_for_host(self, host):
        assert isinstance(host, VictimHost)

        if not self.local_port:
            return

        ip_match = get_interface_to_target(host.ip_addr)
        host.default_tunnel = '%s:%d' % (ip_match, self.local_port)

    def stop(self):
        self._stopped = True
