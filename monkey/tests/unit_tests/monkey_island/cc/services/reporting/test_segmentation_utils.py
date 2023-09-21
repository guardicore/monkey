from ipaddress import IPv4Address

from common.network.network_range import CidrRange
from monkey_island.cc.services.reporting.segmentation_utils import get_ip_if_in_subnet

SUBNET = CidrRange("10.10.2.0/24")


def test_get_ip_if_in_subnet__none_if_not_in_subnet():
    ip = get_ip_if_in_subnet([IPv4Address("10.10.1.1")], SUBNET)

    assert ip is None


def test_get_ip_if_in_subnet():
    IP = IPv4Address("10.10.2.1")
    ip = get_ip_if_in_subnet([IP], SUBNET)

    assert ip == IP
