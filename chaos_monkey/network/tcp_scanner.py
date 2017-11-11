from random import shuffle

from network import HostScanner, HostFinger
from network.tools import check_tcp_ports

__author__ = 'itamar'

BANNER_READ = 1024


class TcpScanner(HostScanner, HostFinger):
    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def is_host_alive(self, host):
        return self.get_host_fingerprint(host, True)

    def get_host_fingerprint(self, host, only_one_port=False):
        """
        Scans a target host to see if it's alive using the tcp_target_ports specified in the configuration.
        :param host: VictimHost structure
        :param only_one_port: Currently unused.
        :return: T/F if there is at least one open port. In addition, the host object is updated to mark those services as alive.
        """

        # maybe hide under really bad detection systems
        target_ports = self._config.tcp_target_ports[:]
        shuffle(target_ports)

        ports, banners = check_tcp_ports(host.ip_addr, target_ports, self._config.tcp_scan_timeout / 1000.0)
        if len(ports) != 0:
            for target_port, banner in zip(ports, banners):
                service = 'tcp-' + str(target_port)
                host.services[service] = {}
                if banner:
                    host.services[service]['banner'] = banner
                if only_one_port:
                    break

        return len(ports) != 0
