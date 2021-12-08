from typing import List

from common.network.network_range import NetworkRange


def compile_scan_target_list(
    local_ips: List[str],
    ranges_to_scan: List[str],
    inaccessible_subnets: List[str],
    blocklisted_ips: List[str],
    enable_local_network_scan: bool,
) -> List[str]:
    scan_target_list = _get_ips_from_ranges_to_scan(ranges_to_scan)

    return scan_target_list


def _get_ips_from_ranges_to_scan(ranges_to_scan):
    scan_target_list = []

    network_ranges = [NetworkRange.get_range_obj(_range) for _range in ranges_to_scan]
    for _range in network_ranges:
        scan_target_list.extend([ip for ip in _range])

    return scan_target_list
