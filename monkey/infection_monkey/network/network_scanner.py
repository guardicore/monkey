import sys
import itertools
import time
if sys.platform.startswith("win"):
    from multiprocessing.dummy import Pool
else:
    from multiprocessing import Pool
from common.network.network_range import *
from infection_monkey.config import WormConfiguration
from infection_monkey.network.info import local_ips, get_interfaces_ranges
from infection_monkey.model import VictimHost
from infection_monkey.network import TcpScanner, PingScanner

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

SCAN_DELAY = 0
ITERATION_BLOCK_SIZE = 5


def _grouper(iterables, chunk_size):
    """
    Goes over an iterable using chunks
    :param iterables: a sequence of iterable objects
    :param chunk_size:  Chunk size, last chunk may be smaller
    :return:
    """
    iterable = itertools.chain(*iterables)
    while True:
        group = tuple(itertools.islice(iterable, chunk_size))
        if not group:
            break
        yield group


class NetworkScanner(object):
    def __init__(self):
        self._ip_addresses = None
        self._ranges = None
        self.scanners = [TcpScanner(), PingScanner()]

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
                if NetworkScanner._is_any_ip_in_subnet([unicode(x) for x in self._ip_addresses], subnet_str):
                    # If machine has IPs from 2 different subnets in the same group, there's no point checking the other
                    # subnet.
                    for other_subnet_str in WormConfiguration.inaccessible_subnets:
                        if other_subnet_str == subnet_str:
                            continue
                        if not NetworkScanner._is_any_ip_in_subnet([unicode(x) for x in self._ip_addresses],
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
        pool = Pool()
        victims_count = 0
        for network_chunk in _grouper(self._ranges, ITERATION_BLOCK_SIZE):
            LOG.debug("Scanning for potential victims in chunk %r", network_chunk)
            victim_chunk = []
            for address in network_chunk:
                # if hasattr(net_range, 'domain_name'):
                #    victim = VictimHost(address, net_range.domain_name)
                # else:
                victim = VictimHost(address)

                victim_chunk.append(victim)
            # skip self IP addresses
            victim_chunk = [x for x in victim_chunk if x.ip_addr not in self._ip_addresses]
            # skip IPs marked as blocked

            bad_victims = [x for x in victim_chunk if x.ip_addr in WormConfiguration.blocked_ips]
            for victim in bad_victims:
                LOG.info("Skipping %s due to blacklist" % victim)
            victim_chunk = [x for x in victim_chunk if x.ip_addr not in WormConfiguration.blocked_ips]

            # check before running scans
            if stop_callback and stop_callback():
                LOG.debug("Got stop signal")
                break

            results = pool.map(self.scan_machine, victim_chunk)
            resulting_victims = [x for x in results if x]  # filter out dead addresses
            for victim in resulting_victims:
                LOG.debug("Found potential victim: %r", victim)
                victims_count += 1
                yield victim

                if victims_count >= max_find:
                    LOG.debug("Found max needed victims (%d), stopping scan", max_find)

                    break
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
        Scans specific machine using given scanner
        :param victim: VictimHost machine
        :return: Victim or None if victim isn't alive
        """
        LOG.debug("Scanning target address: %r", victim)
        if any([scanner.is_host_alive(victim.ip_addr) for scanner in self.scanners]):
            LOG.debug("Found potential target_ip: %r", victim)
            return victim
        else:
            return None

    def on_island(self, server):
        return bool([x for x in self._ip_addresses if x in server])
