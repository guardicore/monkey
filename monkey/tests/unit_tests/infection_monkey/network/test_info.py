from dataclasses import dataclass
from typing import Tuple

import pytest

from infection_monkey.network.info import TCPPortSelector
from infection_monkey.network.ports import COMMON_PORTS


@dataclass
class Connection:
    laddr: Tuple[str, int]


@pytest.mark.parametrize("port", COMMON_PORTS)
def test_tcp_port_selector__checks_common_ports(port: int, monkeypatch):
    tcp_port_selector = TCPPortSelector()
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS if p is not port]

    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )
    assert tcp_port_selector.get_free_tcp_port() is port


def test_tcp_port_selector__checks_other_ports_if_common_ports_unavailable(monkeypatch):
    tcp_port_selector = TCPPortSelector()
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert tcp_port_selector.get_free_tcp_port() is not None


def test_tcp_port_selector__none_if_no_available_ports(monkeypatch):
    tcp_port_selector = TCPPortSelector()
    unavailable_ports = [Connection(("", p)) for p in range(65535)]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert tcp_port_selector.get_free_tcp_port() is None


@pytest.mark.parametrize("common_port", COMMON_PORTS)
def test_tcp_port_selector__checks_common_ports_leases(common_port: int, monkeypatch):
    tcp_port_selector = TCPPortSelector()
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS if p is not common_port]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    free_port_1 = tcp_port_selector.get_free_tcp_port()
    free_port_2 = tcp_port_selector.get_free_tcp_port()

    assert free_port_1 == common_port
    assert free_port_2 != common_port
    assert free_port_2 is not None
    assert free_port_2 not in COMMON_PORTS
