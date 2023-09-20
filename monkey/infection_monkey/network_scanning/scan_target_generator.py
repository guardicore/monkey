import itertools
import logging
import socket
from ipaddress import IPv4Interface
from typing import Dict, Iterable, List, Optional, Sequence

from common.network.network_range import InvalidNetworkRangeError, NetworkRange
from infection_monkey.network import NetworkAddress

logger = logging.getLogger(__name__)


def compile_scan_target_list(
    local_network_interfaces: Sequence[IPv4Interface],
    ranges_to_scan: Sequence[str],
    inaccessible_subnets: Sequence[str],
    blocklisted_ips: Sequence[str],
    scan_my_networks: bool,
) -> List[NetworkAddress]:
    scan_targets = _get_ips_from_subnets_to_scan(ranges_to_scan)

    if scan_my_networks:
        scan_targets.extend(_get_ips_to_scan_from_interface(local_network_interfaces))

    if inaccessible_subnets:
        other_targets = _get_segmentation_check_targets(
            inaccessible_subnets, local_network_interfaces
        )
        scan_targets.extend(other_targets)

    scan_targets = _remove_interface_ips(scan_targets, local_network_interfaces)
    scan_targets = _remove_blocklisted_ips(scan_targets, blocklisted_ips)
    scan_targets = _remove_redundant_targets(scan_targets)
    scan_targets.sort(key=lambda network_address: socket.inet_aton(network_address.ip))

    return scan_targets


def _remove_redundant_targets(targets: Sequence[NetworkAddress]) -> List[NetworkAddress]:
    reverse_dns: Dict[str, Optional[str]] = {}
    for target in targets:
        domain_name = target.domain
        ip = target.ip
        if ip not in reverse_dns or (reverse_dns[ip] is None and domain_name is not None):
            reverse_dns[ip] = domain_name
    return [NetworkAddress(key, value) for (key, value) in reverse_dns.items()]


def _range_to_addresses(range_obj: NetworkRange) -> List[NetworkAddress]:
    addresses = []
    for address in range_obj:
        try:
            domain = range_obj.domain_name  # type: ignore
        except AttributeError:
            domain = None
        addresses.append(NetworkAddress(address, domain))
    return addresses


def _get_ips_from_subnets_to_scan(subnets_to_scan: Iterable[str]) -> List[NetworkAddress]:
    ranges_to_scan = NetworkRange.filter_invalid_ranges(
        subnets_to_scan, "Bad network range input for targets to scan:"
    )

    network_ranges = [NetworkRange.get_range_obj(_range) for _range in ranges_to_scan]
    return _get_ips_from_ranges_to_scan(network_ranges)


def _get_ips_from_ranges_to_scan(network_ranges: Iterable[NetworkRange]) -> List[NetworkAddress]:
    scan_targets = []

    for _range in network_ranges:
        scan_targets.extend(_range_to_addresses(_range))
    return scan_targets


def _get_ips_to_scan_from_interface(
    interfaces: Sequence[IPv4Interface],
) -> List[NetworkAddress]:
    ranges = [str(interface) for interface in interfaces]

    ranges = NetworkRange.filter_invalid_ranges(
        ranges, "Local network interface returns an invalid IP:"
    )
    return _get_ips_from_subnets_to_scan(ranges)


def _remove_interface_ips(
    scan_targets: Sequence[NetworkAddress], interfaces: Iterable[IPv4Interface]
) -> List[NetworkAddress]:
    interface_ips = [str(interface.ip) for interface in interfaces]
    return _remove_ips_from_scan_targets(scan_targets, interface_ips)


def _remove_blocklisted_ips(
    scan_targets: Sequence[NetworkAddress], blocked_ips: Sequence[str]
) -> List[NetworkAddress]:
    filtered_blocked_ips = NetworkRange.filter_invalid_ranges(
        blocked_ips, "Invalid blocked IP provided:"
    )
    if len(filtered_blocked_ips) != len(blocked_ips):
        raise InvalidNetworkRangeError("Received an invalid blocked IP. Aborting just in case.")
    return _remove_ips_from_scan_targets(scan_targets, filtered_blocked_ips)


def _remove_ips_from_scan_targets(
    scan_targets: Sequence[NetworkAddress], ips_to_remove: Iterable[str]
) -> List[NetworkAddress]:
    ips_to_remove_set = set(ips_to_remove)
    return [address for address in scan_targets if address.ip not in ips_to_remove_set]


def _get_segmentation_check_targets(
    inaccessible_subnets: Iterable[str], local_interfaces: Iterable[IPv4Interface]
) -> List[NetworkAddress]:
    ips_to_scan = []
    local_ips = [str(interface.ip) for interface in local_interfaces]

    local_ips = NetworkRange.filter_invalid_ranges(local_ips, "Invalid local IP found: ")
    inaccessible_subnets = NetworkRange.filter_invalid_ranges(
        inaccessible_subnets, "Invalid segmentation scan target: "
    )

    inaccessible_ranges = _convert_to_range_object(inaccessible_subnets)
    subnet_pairs = itertools.product(inaccessible_ranges, inaccessible_ranges)

    for subnet1, subnet2 in subnet_pairs:
        if _is_segmentation_check_required(local_ips, subnet1, subnet2):
            ips = _get_ips_from_ranges_to_scan([subnet2])
            ips_to_scan.extend(ips)

    return ips_to_scan


def _convert_to_range_object(subnets: Iterable[str]) -> List[NetworkRange]:
    return [NetworkRange.get_range_obj(subnet) for subnet in subnets]


def _is_segmentation_check_required(
    local_ips: Sequence[str], subnet1: NetworkRange, subnet2: NetworkRange
):
    return _is_any_ip_in_subnet(local_ips, subnet1) and not _is_any_ip_in_subnet(local_ips, subnet2)


def _is_any_ip_in_subnet(ip_addresses: Iterable[str], subnet: NetworkRange):
    for ip_address in ip_addresses:
        if subnet.is_in_range(ip_address):
            return True
    return False
