import re

from marshmallow import ValidationError

ip_regex = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
cird_notation_regex = r"([0-9]|1[0-9]|2[0-9]|3[0-2])"
hostname_regex = r"([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*.?)*([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*)"


def validate_subnet_range(subnet_range: str):
    range_regexes = [
        "^" + ip_regex + "$|",
        "^" + ip_regex + r"\s*-\s*" + ip_regex + "$|",
        "^" + ip_regex + "/" + cird_notation_regex + "$|",
        "^" + hostname_regex + "$",
    ]
    range_regexes = re.compile("".join(range_regexes))
    if not re.match(range_regexes, subnet_range):
        raise ValidationError(f"Invalid subnet range {subnet_range}")


def validate_ip(ip: str):
    if not re.match(re.compile("".join(["^", ip_regex, "$"])), ip):
        raise ValidationError(f"Invalid ip address {ip}")
