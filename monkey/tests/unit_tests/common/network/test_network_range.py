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


def test_check_if_hostname():
    valid_hostnames = [
        "example.com",
        "myserver",
        "mailserver.domain",
        "subdomain.example.org",
        "my-host",
        "ftp-server",
        "test123",
        "web1.example.net",
        "mail.domain.com",
        "secure-server",
    ]

    invalid_hostnames = [
        "-invalid",
        "spaces not allowed",
        "underscore_invalid",
        "too-long-hostname-" + "x" * 250,
        "x" * 65 + ".long.domain",
        "invalid..domain",
        "invalid@character",
        "host name with spaces",
        "hostname!",
        "192.168.0.1",  # IP address format
        "localhost.localdomain.",  # Trailing dot
        "localhost-",  # Trailing dash
        "domain.name.ending.123456",  # TLD ending with all-numeric
    ]

    for hostname in valid_hostnames:
        assert NetworkRange.check_if_hostname(hostname)

    for hostname in invalid_hostnames:
        assert not NetworkRange.check_if_hostname(hostname)
