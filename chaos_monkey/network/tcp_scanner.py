
import time
import socket
from network import HostScanner
from model.host import VictimHost

__author__ = 'itamar'

class TcpScanner(HostScanner):
    def __init__(self, target_port=None):
        self._config = __import__('config').WormConfiguration

    def is_host_alive(self, host):
        assert isinstance(host, VictimHost)

        for target_port in self._config.tcp_target_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._config.tcp_scan_timeout / 1000.0)

            try:
                sock.connect((host.ip_addr, target_port))
                sock.close()
                return True
            except socket.error:
                time.sleep(self._config.tcp_scan_interval / 1000.0)

                continue

        return False