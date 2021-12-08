import pytest

from infection_monkey.network.scan_target_generator import compile_scan_target_list


def compile_ranges_only(ranges):
    return compile_scan_target_list(
        local_ips=[],
        ranges_to_scan=ranges,
        inaccessible_subnets=[],
        blocklisted_ips=[],
        enable_local_network_scan=False,
    )


def test_single_subnet():
    scan_targets = compile_ranges_only(["10.0.0.0/24"])

    assert len(scan_targets) == 255

    for i in range(0, 255):
        assert f"10.0.0.{i}" in scan_targets


@pytest.mark.parametrize("single_ip", ["10.0.0.2", "10.0.0.2/32", "10.0.0.2-10.0.0.2"])
def test_single_ip(single_ip):
    print(single_ip)
    scan_targets = compile_ranges_only([single_ip])

    assert len(scan_targets) == 1
    assert "10.0.0.2" in scan_targets
    assert "10.0.0.2" == scan_targets[0]


def test_multiple_subnet():
    scan_targets = compile_ranges_only(["10.0.0.0/24", "192.168.56.8/29"])

    assert len(scan_targets) == 262

    for i in range(0, 255):
        assert f"10.0.0.{i}" in scan_targets

    for i in range(8, 15):
        assert f"192.168.56.{i}" in scan_targets


def test_middle_of_range_subnet():
    scan_targets = compile_ranges_only(["192.168.56.4/29"])

    assert len(scan_targets) == 7

    for i in range(0, 7):
        assert f"192.168.56.{i}" in scan_targets


@pytest.mark.parametrize(
    "ip_range", ["192.168.56.25-192.168.56.33", "192.168.56.25 - 192.168.56.33"]
)
def test_ip_range(ip_range):
    scan_targets = compile_ranges_only([ip_range])

    assert len(scan_targets) == 9

    for i in range(25, 34):
        assert f"192.168.56.{i}" in scan_targets


def test_no_duplicates():
    scan_targets = compile_ranges_only(["192.168.56.0/29", "192.168.56.2", "192.168.56.4"])

    assert len(scan_targets) == 7

    for i in range(0, 7):
        assert f"192.168.56.{i}" in scan_targets


def test_blocklisted_ips():
    blocklisted_ips = ["10.0.0.5", "10.0.0.32", "10.0.0.119", "192.168.1.33"]

    scan_targets = compile_scan_target_list(
        local_ips=[],
        ranges_to_scan=["10.0.0.0/24"],
        inaccessible_subnets=[],
        blocklisted_ips=blocklisted_ips,
        enable_local_network_scan=False,
    )

    assert len(scan_targets) == 252
    for blocked_ip in blocklisted_ips:
        assert blocked_ip not in scan_targets


@pytest.mark.parametrize("ranges_to_scan", [["10.0.0.5"], []])
def test_only_ip_blocklisted(ranges_to_scan):
    blocklisted_ips = ["10.0.0.5"]

    scan_targets = compile_scan_target_list(
        local_ips=[],
        ranges_to_scan=ranges_to_scan,
        inaccessible_subnets=[],
        blocklisted_ips=blocklisted_ips,
        enable_local_network_scan=False,
    )

    assert len(scan_targets) == 0


def test_local_ips_removed_from_targets():
    local_ips = ["10.0.0.5", "10.0.0.32", "10.0.0.119", "192.168.1.33"]

    scan_targets = compile_scan_target_list(
        local_ips=local_ips,
        ranges_to_scan=["10.0.0.0/24"],
        inaccessible_subnets=[],
        blocklisted_ips=[],
        enable_local_network_scan=False,
    )

    assert len(scan_targets) == 252
    for ip in local_ips:
        assert ip not in scan_targets


@pytest.mark.parametrize("ranges_to_scan", [["10.0.0.5"], []])
def test_only_scan_ip_is_local(ranges_to_scan):
    local_ips = ["10.0.0.5", "10.0.0.32", "10.0.0.119", "192.168.1.33"]

    scan_targets = compile_scan_target_list(
        local_ips=local_ips,
        ranges_to_scan=ranges_to_scan,
        inaccessible_subnets=[],
        blocklisted_ips=[],
        enable_local_network_scan=False,
    )

    assert len(scan_targets) == 0


def test_local_ips_and_blocked_ips_removed_from_targets():
    local_ips = ["10.0.0.5", "10.0.0.32", "10.0.0.119", "192.168.1.33"]
    blocked_ips = ["10.0.0.63", "192.168.1.77", "0.0.0.0"]

    scan_targets = compile_scan_target_list(
        local_ips=local_ips,
        ranges_to_scan=["10.0.0.0/24", "192.168.1.0/24"],
        inaccessible_subnets=[],
        blocklisted_ips=blocked_ips,
        enable_local_network_scan=False,
    )

    assert len(scan_targets) == (2 * (256 - 1)) - len(local_ips) - (len(blocked_ips) - 1)

    for ip in local_ips:
        assert ip not in scan_targets

    for ip in blocked_ips:
        assert ip not in scan_targets
