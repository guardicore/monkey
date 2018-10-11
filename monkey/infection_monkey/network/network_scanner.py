import logging
import time

from common.network.network_range import *
from infection_monkey.config import WormConfiguration
from infection_monkey.network.info import local_ips, get_interfaces_ranges
from infection_monkey.model import VictimHost
from infection_monkey.control import ControlClient
from infection_monkey.network.tools import traceroute

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

SCAN_DELAY = 0


class NetworkScanner(object):
    def __init__(self):
        self._ip_addresses = None

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

    @staticmethod
    def get_k8s_node_subnet(system_info):
        """
        Gets suspected subnet of k8s nodes.
        Second hop of traceroute out of a pod is usually in class C with k8s nodes.
        :param system_info: system_info returned from system_info_collector.
        :return: Suspected subnet of k8s nodes or None if machine is not a k8s pod.
        """
        if system_info and system_info.get('k8s', {'is_pod': False})['is_pod']:
            route = traceroute('google.com', 2)
            if len(route) >= 2:
                return CidrRange(str(route[-1]) + '/24')

        return None

    def generate_ranges(self, system_info):
        """
        Generates network ranges to scan. Re-queries the island's config after iterating over all ranges in local config
        :return: yields network range
        """
        old_range_strs = set()
        range_strs = set()

        while True:
            old_range_strs = old_range_strs.union(range_strs)
            ControlClient.load_control_config()
            range_strs = set(WormConfiguration.subnet_scan_list + WormConfiguration.dynamic_subnet_scan_list)
            range_strs = range_strs.difference(old_range_strs)

            if not range_strs:
                break

            for range_str in range_strs:
                yield NetworkRange.get_range_obj(address_str=range_str)

        if WormConfiguration.local_network_scan:
            for net_range in get_interfaces_ranges():
                yield net_range

        k8s_node_subnet = NetworkScanner.get_k8s_node_subnet(system_info)
        if k8s_node_subnet:
            yield k8s_node_subnet

        for net_range in self._get_inaccessible_subnets_ips():
            yield net_range

    def get_victim_machines(self, scan_type, max_find=5, stop_callback=None, system_info=None):
        """
        Finds machines according to the ranges specified in the object
        :param scan_type: A hostscanner class, will be instanced and used to scan for new machines
        :param max_find: Max number of victims to find regardless of ranges
        :param stop_callback: A callback to check at any point if we should stop scanning
        :param system_info: system_info returned from system_info_collector
        :return: yields a sequence of VictimHost instances
        """
        if not scan_type:
            return

        scanner = scan_type()
        victims_count = 0

        for net_range in self.generate_ranges(system_info):
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

    @staticmethod
    def _is_any_ip_in_subnet(ip_addresses, subnet_str):
        for ip_address in ip_addresses:
            if NetworkRange.get_range_obj(subnet_str).is_in_range(ip_address):
                return True
        return False
