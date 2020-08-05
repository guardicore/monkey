import logging
import time
from multiprocessing.dummy import Pool

from common.network.network_range import NetworkRange
from infection_monkey.config import WormConfiguration
from infection_monkey.model.victim_host_generator import VictimHostGenerator
from infection_monkey.network.info import get_interfaces_ranges, local_ips
from infection_monkey.network.ping_scanner import PingScanner
from infection_monkey.network.tcp_scanner import TcpScanner

LOG = logging.getLogger(__name__)

ITERATION_BLOCK_SIZE = 5


class NetworkScanner(object):
    def __init__(self):
        self._ip_addresses = None
        self._ranges = None
        self.scanners = [TcpScanner(), PingScanner()]

    def initialize(self):
        """
        Set up scanning.
        based on configuration: scans local network and/or scans fixed list of IPs/subnets.
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
        self._ranges += self._get_inaccessible_subnets_ips()
        LOG.info("Base local networks to scan are: %r", self._ranges)

    def _get_inaccessible_subnets_ips(self):
        """
        For each of the machine's IPs, checks if it's in one of the subnets specified in the
        'inaccessible_subnets' config value. If so, all other subnets in the config value shouldn't be accessible.
        All these subnets are returned.
        :return: A list of subnets that shouldn't be accessible from the machine the monkey is running on.
        """
        subnets_to_scan = []
        if len(WormConfiguration.inaccessible_subnets) > 1:
            for subnet_str in WormConfiguration.inaccessible_subnets:
                if NetworkScanner._is_any_ip_in_subnet([str(x) for x in self._ip_addresses], subnet_str):
                    # If machine has IPs from 2 different subnets in the same group, there's no point checking the other
                    # subnet.
                    for other_subnet_str in WormConfiguration.inaccessible_subnets:
                        if other_subnet_str == subnet_str:
                            continue
                        if not NetworkScanner._is_any_ip_in_subnet([str(x) for x in self._ip_addresses],
                                                                   other_subnet_str):
                            subnets_to_scan.append(NetworkRange.get_range_obj(other_subnet_str))
                    break

        return subnets_to_scan

    def get_victim_machines(self, max_find=5, stop_callback=None):
        """
        Finds machines according to the ranges specified in the object
        :param max_find: Max number of victims to find regardless of ranges
        :param stop_callback: A callback to check at any point if we should stop scanning
        :return: yields a sequence of VictimHost instances
        """
        # We currently use the ITERATION_BLOCK_SIZE as the pool size, however, this may not be the best decision
        # However, the decision what ITERATION_BLOCK_SIZE also requires balancing network usage (pps and bw)
        # Because we are using this to spread out IO heavy tasks, we can probably go a lot higher than CPU core size
        # But again, balance
        pool = Pool(ITERATION_BLOCK_SIZE)
        victim_generator = VictimHostGenerator(self._ranges, WormConfiguration.blocked_ips, local_ips())

        victims_count = 0
        for victim_chunk in victim_generator.generate_victims(ITERATION_BLOCK_SIZE):
            LOG.debug("Scanning for potential victims in chunk %r", victim_chunk)

            # check before running scans
            if stop_callback and stop_callback():
                LOG.debug("Got stop signal")
                return

            results = pool.map(self.scan_machine, victim_chunk)
            resulting_victims = [x for x in results if x is not None]
            for victim in resulting_victims:
                LOG.debug("Found potential victim: %r", victim)
                victims_count += 1
                yield victim

                if victims_count >= max_find:
                    LOG.debug("Found max needed victims (%d), stopping scan", max_find)
                    return
            if WormConfiguration.tcp_scan_interval:
                # time.sleep uses seconds, while config is in milliseconds
                time.sleep(WormConfiguration.tcp_scan_interval / float(1000))

    @staticmethod
    def _is_any_ip_in_subnet(ip_addresses, subnet_str):
        for ip_address in ip_addresses:
            if NetworkRange.get_range_obj(subnet_str).is_in_range(ip_address):
                return True
        return False

    def scan_machine(self, victim):
        """
        Scans specific machine using instance scanners
        :param victim: VictimHost machine
        :return: Victim or None if victim isn't alive
        """
        LOG.debug("Scanning target address: %r", victim)
        if any([scanner.is_host_alive(victim) for scanner in self.scanners]):
            LOG.debug("Found potential target_ip: %r", victim)
            return victim
        else:
            return None

    def on_island(self, server):
        return bool([x for x in self._ip_addresses if x in server])
