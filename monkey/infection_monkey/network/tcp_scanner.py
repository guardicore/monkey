from itertools import izip_longest
from random import shuffle

import infection_monkey.config
from infection_monkey.network import HostScanner, HostFinger
from infection_monkey.network.tools import check_tcp_ports, tcp_port_to_service
from infection_monkey.transport.attack_telems.victim_host_telem import VictimHostTelem
from common.utils.attack_utils import ScanStatus

__author__ = 'itamar'

BANNER_READ = 1024


class TcpScanner(HostScanner, HostFinger):

    _SCANNED_SERVICE = 'unknown(TCP)'

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration

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

        ports, banners = check_tcp_ports(host.ip_addr, target_ports, self._config.tcp_scan_timeout / 1000.0,
                                         self._config.tcp_scan_get_banner)
        for target_port, banner in izip_longest(ports, banners, fillvalue=None):
            service = tcp_port_to_service(target_port)
            host.services[service] = {}
            host.services[service].update(self.format_service_info(port=target_port))
            if banner:
                host.services[service]['banner'] = banner
            if only_one_port:
                break

        return len(ports) != 0
