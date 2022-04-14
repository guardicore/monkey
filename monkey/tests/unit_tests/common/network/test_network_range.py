from common.network.network_range import NetworkRange


def test_range_filtering():
    invalid_ranges = [
        # Invalid IP segment
        "172.60.999.109",
        "172.60.-1.109",
        "172.60.999.109 - 172.60.1.109",
        "172.60.999.109/32",
        "172.60.999.109/24",
        # Invalid CIDR
        "172.60.1.109/33",
        "172.60.1.109/-1",
        # Typos
        "172.60.9.109 -t 172.60.1.109",
        "172.60..9.109",
        "172.60,9.109",
        " 172.60 .9.109 ",
    ]

    valid_ranges = [
        " 172.60.9.109 ",
        "172.60.9.109 - 172.60.1.109",
        "172.60.9.109- 172.60.1.109",
        "0.0.0.0",
        "localhost",
    ]

    invalid_ranges.extend(valid_ranges)

    remaining = NetworkRange.filter_invalid_ranges(invalid_ranges, "Test error:")
    for _range in remaining:
        assert _range in valid_ranges
    assert len(remaining) == len(valid_ranges)
