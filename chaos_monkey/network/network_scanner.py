import time
import logging
from . import HostScanner
from config import WormConfiguration
from info import local_ips, get_ips_from_interfaces
from range import *

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

SCAN_DELAY = 0


class NetworkScanner(object):
    def __init__(self):
        self._ip_addresses = None
        self._ranges = None

    def initialize(self):
        # get local ip addresses
        self._ip_addresses = local_ips()

        if not self._ip_addresses:
            raise Exception("Cannot find local IP address for the machine")

        LOG.info("Found local IP addresses of the machine: %r", self._ip_addresses)
        # for fixed range, only scan once.
        if WormConfiguration.range_class is FixedRange:
            self._ranges = [WormConfiguration.range_class(None)]
        else:
            self._ranges = [WormConfiguration.range_class(ip_address)
                            for ip_address in self._ip_addresses]
        if WormConfiguration.local_network_scan:
            self._ranges += [FixedRange([ip_address for ip_address in get_ips_from_interfaces()])]
        LOG.info("Base local networks to scan are: %r", self._ranges)

    def get_victim_machines(self, scan_type, max_find=5, stop_callback=None):
        assert issubclass(scan_type, HostScanner)

        scanner = scan_type()
        victims_count = 0

        for range in self._ranges:
            LOG.debug("Scanning for potential victims in the network %r", range)
            for victim in range:
                if stop_callback and stop_callback():
                    LOG.debug("Got stop signal")
                    break

                # skip self IP address
                if victim.ip_addr in self._ip_addresses:
                    continue

                LOG.debug("Scanning %r...", victim)

                # if scanner detect machine is up, add it to victims list
                if scanner.is_host_alive(victim):
                    LOG.debug("Found potential victim: %r", victim)
                    victims_count += 1
                    yield victim

                    if victims_count >= max_find:
                        LOG.debug("Found max needed victims (%d), stopping scan", max_find)

                        break

                if SCAN_DELAY:
                    time.sleep(SCAN_DELAY)
