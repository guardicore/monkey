import logging
import time

from common.network.network_range import *
from infection_monkey.config import WormConfiguration
from infection_monkey.network.info import local_ips, get_interfaces_ranges
from infection_monkey.model import VictimHost
from infection_monkey.network import HostScanner

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

SCAN_DELAY = 0


class NetworkScanner(object):
    def __init__(self):
        self._ip_addresses = None
        self._ranges = None

    def initialize(self):
        """
        Set up scanning.
        based on configuration: scans local network and/or scans fixed list of IPs/subnets.
        :return:
        """
        # get local ip addresses
        self._ip_addresses = local_ips()

        if not self._ip_addresses:
            raise Exception("Cannot find local IP address for the machine")

        LOG.info("Found local IP addresses of the machine: %r", self._ip_addresses)
        # for fixed range, only scan once.
        self._ranges = [NetworkRange.get_range_obj(address_str=x) for x in WormConfiguration.subnet_scan_list]
        if WormConfiguration.local_network_scan:
            self._ranges += get_interfaces_ranges()
        LOG.info("Base local networks to scan are: %r", self._ranges)

    def get_victim_machines(self, scan_type, max_find=5, stop_callback=None):
        assert issubclass(scan_type, HostScanner)

        scanner = scan_type()
        victims_count = 0

        for net_range in self._ranges:
            LOG.debug("Scanning for potential victims in the network %r", net_range)
            for ip_addr in net_range:
                victim = VictimHost(ip_addr)
                if stop_callback and stop_callback():
                    LOG.debug("Got stop signal")
                    break

                # skip self IP address
                if victim.ip_addr in self._ip_addresses:
                    continue

                # skip IPs marked as blocked
                if victim.ip_addr in WormConfiguration.blocked_ips:
                    LOG.info("Skipping %s due to blacklist" % victim)
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
