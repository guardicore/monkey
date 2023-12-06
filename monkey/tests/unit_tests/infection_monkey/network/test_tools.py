from ipaddress import IPv4Address, IPv4Interface
from types import MappingProxyType

import pytest

from infection_monkey.network.tools import get_interface_to_target

INTERFACES = (
    IPv4Interface("192.168.1.0/24"),
    IPv4Interface("192.168.2.2/32"),
    IPv4Interface("10.0.0.0/16"),
)

INCLUDED_IPS = MappingProxyType(
    {
        IPv4Address("192.168.1.10"): INTERFACES[0],
        IPv4Address("192.168.1.254"): INTERFACES[0],
        IPv4Address("192.168.2.2"): INTERFACES[1],
        IPv4Address("10.0.254.5"): INTERFACES[2],
        IPv4Address("10.0.0.1"): INTERFACES[2],
        IPv4Address("10.0.16.123"): INTERFACES[2],
    }
)

EXCLUDED_IPS = (
    IPv4Address("192.168.2.10"),
    IPv4Address("192.168.2.3"),
    IPv4Address("192.168.3.4"),
    IPv4Address("172.1.2.3"),
    IPv4Address("10.1.254.5"),
    IPv4Address("10.2.0.1"),
    IPv4Address("10.3.16.123"),
)


def test_empty_interfaces(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.network.tools._empirical_get_interface_to_target",
        lambda *args, **kwargs: None,
    )
    assert get_interface_to_target([], IPv4Address("192.168.1.10")) is None


@pytest.mark.parametrize("ip", INCLUDED_IPS.keys())
def test_target_reachable(ip):
    assert get_interface_to_target(INTERFACES, ip) == INCLUDED_IPS[ip]


@pytest.mark.parametrize("ip", EXCLUDED_IPS)
def test_target_unreachable(ip, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.network.tools._empirical_get_interface_to_target",
        lambda *args, **kwargs: None,
    )
    assert get_interface_to_target(INTERFACES, ip) is None


@pytest.mark.parametrize("ip", EXCLUDED_IPS)
def test_empirical_fallback(monkeypatch, ip):
    monkeypatch.setattr(
        "infection_monkey.network.tools._empirical_get_interface_to_target",
        lambda *args, **kwargs: INTERFACES[2].ip,
    )
    # import pudb; pu.db
    assert get_interface_to_target(INTERFACES, ip) == INTERFACES[2]
