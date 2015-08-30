
import time
import socket
import logging
from network import HostScanner
from config import WormConfiguration

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

SCAN_DELAY = 0

class NetworkScanner(object):
    def __init__(self):
        self._ip_addresses = None
        self._ranges = None

    def initialize(self):
        # get local ip addresses
        local_hostname = socket.gethostname()
        self._ip_addresses = socket.gethostbyname_ex(local_hostname)[2]

        if not self._ip_addresses:
            raise Exception("Cannot find local IP address for the machine")

        LOG.info("Found local IP addresses of the machine: %r", self._ip_addresses)

        self._ranges = [WormConfiguration.range_class(ip_address)
                        for ip_address in self._ip_addresses]

        LOG.info("Base local networks to scan are: %r", self._ranges)

    def get_victim_machines(self, scan_type, max_find=5):
        assert issubclass(scan_type, HostScanner)

        scanner = scan_type()
        victims_count = 0

        for range in self._ranges:
            LOG.debug("Scanning for potantional victims in the network %r", range)
            for victim in range:
                # skip self IP address
                if victim.ip_addr in self._ip_addresses:
                    continue

                LOG.debug("Scanning %r...", victim)

                # if scanner detect machine is up, add it to victims list
                if scanner.is_host_alive(victim):
                    LOG.debug("Found potational victim: %r", victim)
                    victims_count += 1
                    yield victim

                    if victims_count >= max_find:
                        LOG.debug("Found max needed victims (%d), stopping scan", max_find)

                        break

                if SCAN_DELAY:
                    time.sleep(SCAN_DELAY)
