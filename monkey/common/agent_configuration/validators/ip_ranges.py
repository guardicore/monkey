import re
from ipaddress import AddressValueError, IPv4Address, IPv4Network, NetmaskValueError


def validate_subnet_range(subnet_range: str):
    try:
        return validate_ip(subnet_range)
    except ValueError:
        pass

    try:
        return validate_ip_range(subnet_range)
    except ValueError:
        pass

    try:
        return validate_ip_network(subnet_range)
    except ValueError:
        pass

    try:
        return validate_hostname(subnet_range)
    except ValueError:
        raise ValueError(f"Invalid subnet range {subnet_range}")


def validate_hostname(hostname: str):
    # Based on hostname syntax: https://www.rfc-editor.org/rfc/rfc1123#page-13
    hostname_segments = hostname.split(".")
    if any((part.endswith("-") or part.startswith("-") for part in hostname_segments)):
        raise ValueError(f"Hostname segment can't start or end with a hyphen: {hostname}")
    if not any((char.isalpha() for char in hostname_segments[-1])):
        raise ValueError(f"Last segment of a hostname must contain a letter: {hostname}")

    valid_characters_pattern = r"^[A-Za-z0-9\-]+$"
    valid_characters_regex = re.compile(valid_characters_pattern)
    matches = (
        re.match(valid_characters_regex, hostname_segment) for hostname_segment in hostname_segments
    )

    if not all(matches):
        raise ValueError(f"Hostname contains invalid characters: {hostname}")


def validate_ip_network(ip_network: str):
    try:
        IPv4Network(ip_network, strict=False)
    except (NetmaskValueError, AddressValueError):
        raise ValueError(f"Invalid IPv4 network {ip_network}")


def validate_ip_range(ip_range: str):
    ip_range = ip_range.replace(" ", "")
    ips = ip_range.split("-")
    if len(ips) != 2:
        raise ValueError(f"Invalid IP range {ip_range}")
    validate_ip(ips[0])
    validate_ip(ips[1])


def validate_ip(ip: str):
    try:
        IPv4Address(ip)
    except AddressValueError:
        raise ValueError(f"Invalid IP address {ip}")
