import itertools
import logging
from collections import namedtuple
from typing import List, Set

from common.network.network_range import InvalidNetworkRangeError, NetworkRange

NetworkInterface = namedtuple("NetworkInterface", ("address", "netmask"))


logger = logging.getLogger(__name__)


def compile_scan_target_list(
    local_network_interfaces: List[NetworkInterface],
    ranges_to_scan: List[str],
    inaccessible_subnets: List[str],
    blocklisted_ips: List[str],
    enable_local_network_scan: bool,
) -> List[str]:

    scan_targets = _get_ips_from_ranges_to_scan(ranges_to_scan)

    if enable_local_network_scan:
        scan_targets.update(_get_ips_to_scan_from_local_interface(local_network_interfaces))

    if inaccessible_subnets:
        inaccessible_subnets = _get_segmentation_check_targets(
            inaccessible_subnets, local_network_interfaces
        )
        scan_targets.update(inaccessible_subnets)

    _remove_interface_ips(scan_targets, local_network_interfaces)
    _remove_blocklisted_ips(scan_targets, blocklisted_ips)

    scan_target_list = list(scan_targets)
    scan_target_list.sort()

    return scan_target_list


def _get_ips_from_ranges_to_scan(ranges_to_scan: List[str]) -> Set[str]:
    scan_targets = set()

    ranges_to_scan = _filter_invalid_ranges(
        ranges_to_scan, "Bad network range input for targets to scan:"
    )

    network_ranges = [NetworkRange.get_range_obj(_range) for _range in ranges_to_scan]
    for _range in network_ranges:
        scan_targets.update(set(_range))
    return scan_targets


def _get_ips_to_scan_from_local_interface(interfaces: List[NetworkInterface]) -> Set[str]:
    ranges = [f"{interface.address}{interface.netmask}" for interface in interfaces]

    ranges = _filter_invalid_ranges(ranges, "Local network interface returns an invalid IP:")
    return _get_ips_from_ranges_to_scan(ranges)


def _remove_interface_ips(scan_targets: Set[str], interfaces: List[NetworkInterface]):
    interface_ips = [interface.address for interface in interfaces]
    _remove_ips_from_scan_targets(scan_targets, interface_ips)


def _remove_blocklisted_ips(scan_targets: Set[str], blocked_ips: List[str]):
    filtered_blocked_ips = _filter_invalid_ranges(blocked_ips, "Invalid blocked IP provided:")
    if not len(filtered_blocked_ips) == len(blocked_ips):
        raise InvalidNetworkRangeError("Received an invalid blocked IP. Aborting just in case.")
    _remove_ips_from_scan_targets(scan_targets, blocked_ips)


def _remove_ips_from_scan_targets(scan_targets: Set[str], ips_to_remove: List[str]):
    for ip in ips_to_remove:
        try:
            scan_targets.remove(ip)
        except KeyError:
            # We don't need to remove the ip if it's already missing from the scan_targets
            pass


def _get_segmentation_check_targets(
    inaccessible_subnets: List[str], local_interfaces: List[NetworkInterface]
):
    subnets_to_scan = set()
    local_ips = [interface.address for interface in local_interfaces]

    local_ips = _filter_invalid_ranges(local_ips, "Invalid local IP found: ")
    inaccessible_subnets = _filter_invalid_ranges(
        inaccessible_subnets, "Invalid segmentation scan target: "
    )

    inaccessible_subnets = _convert_to_range_object(inaccessible_subnets)
    subnet_pairs = itertools.product(inaccessible_subnets, inaccessible_subnets)

    for (subnet1, subnet2) in subnet_pairs:
        if _is_segmentation_check_required(local_ips, subnet1, subnet2):
            ips = _get_ips_from_ranges_to_scan(subnet2)
            subnets_to_scan.update(ips)

    return subnets_to_scan


def _filter_invalid_ranges(ranges: List[str], error_msg: str) -> List[str]:
    filtered = []
    for target_range in ranges:
        try:
            NetworkRange.validate_range(target_range)
        except InvalidNetworkRangeError as e:
            logger.error(f"{error_msg} {e}")
            continue
        filtered.append(target_range)
    return filtered


def _convert_to_range_object(subnets: List[str]) -> List[NetworkRange]:
    return [NetworkRange.get_range_obj(subnet) for subnet in subnets]


def _is_segmentation_check_required(
    local_ips: List[str], subnet1: NetworkRange, subnet2: NetworkRange
):
    return _is_any_ip_in_subnet(local_ips, subnet1) and not _is_any_ip_in_subnet(local_ips, subnet2)


def _is_any_ip_in_subnet(ip_addresses: List[str], subnet: NetworkRange):
    for ip_address in ip_addresses:
        if subnet.is_in_range(ip_address):
            return True
    return False
