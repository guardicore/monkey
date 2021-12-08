from typing import List, Set

from common.network.network_range import NetworkRange


def compile_scan_target_list(
    local_ips: List[str],
    ranges_to_scan: List[str],
    inaccessible_subnets: List[str],
    blocklisted_ips: List[str],
    enable_local_network_scan: bool,
) -> List[str]:
    scan_targets = _get_ips_from_ranges_to_scan(ranges_to_scan)

    scan_target_list = list(scan_targets)
    scan_target_list.sort()
    return scan_target_list


def _get_ips_from_ranges_to_scan(ranges_to_scan: List[str]) -> Set[str]:
    scan_targets = set()

    network_ranges = [NetworkRange.get_range_obj(_range) for _range in ranges_to_scan]
    for _range in network_ranges:
        scan_targets.update(set(_range))

    return scan_targets
