import re
from ipaddress import AddressValueError, IPv4Address, IPv4Network, NetmaskValueError

from marshmallow import ValidationError

hostname_pattern = r"([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*.?)*([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*)"
hostname_regex = re.compile(hostname_pattern)


def validate_subnet_range(subnet_range: str):
    try:
        return validate_ip(subnet_range)
    except ValidationError:
        pass

    try:
        return validate_ip_range(subnet_range)
    except ValidationError:
        pass

    try:
        return validate_ip_network(subnet_range)
    except ValidationError:
        pass

    try:
        return validate_hostname(subnet_range)
    except ValidationError:
        raise ValidationError(f"Invalid subnet range {subnet_range}")


def validate_hostname(hostname: str):
    match = re.match(hostname_regex, hostname)
    if match and match.group() == hostname:
        return
    else:
        raise ValidationError(f"Invalid hostname {hostname}")


def validate_ip_network(ip_network: str):
    try:
        IPv4Network(ip_network, strict=False)
        return
    except (NetmaskValueError, AddressValueError):
        raise ValidationError(f"Invalid IPv4 network {ip_network}")


def validate_ip_range(ip_range: str):
    try:
        ip_range = ip_range.replace(" ", "")
        ips = ip_range.split("-")
        validate_ip(ips[0])
        validate_ip(ips[1])
        if len(ips) != 2:
            raise ValidationError(f"Invalid IP range {ip_range}")
    except (AddressValueError, IndexError):
        raise ValidationError(f"Invalid IP range {ip_range}")


def validate_ip(ip: str):
    try:
        IPv4Address(ip)
    except AddressValueError:
        raise ValidationError(f"Invalid IP address {ip}")
