import time
from random import shuffle
from network import HostScanner, HostFinger
from model.host import VictimHost
from network.tools import check_port_tcp

__author__ = 'itamar'

BANNER_READ = 1024


class TcpScanner(HostScanner, HostFinger):
    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def is_host_alive(self, host):
        return self.get_host_fingerprint(host, True)

    def get_host_fingerprint(self, host, only_one_port=False):
        assert isinstance(host, VictimHost)

        count = 0
        # maybe hide under really bad detection systems
        target_ports = self._config.tcp_target_ports[:]
        shuffle(target_ports)

        for target_port in target_ports:

            is_open, banner = check_port_tcp(host.ip_addr,
                                             target_port,
                                             self._config.tcp_scan_timeout / 1000.0,
                                             self._config.tcp_scan_get_banner)

            if is_open:
                count += 1
                service = 'tcp-' + str(target_port)
                host.services[service] = {}
                if banner:
                    host.services[service]['banner'] = banner
                if only_one_port:
                    break
            else:
                time.sleep(self._config.tcp_scan_interval / 1000.0)

        return count != 0
