from dataclasses import dataclass
from typing import Tuple

import pytest

from infection_monkey.network.info import get_free_tcp_port
from infection_monkey.network.ports import COMMON_PORTS


@dataclass
class Connection:
    laddr: Tuple[str, int]


@pytest.mark.parametrize("port", COMMON_PORTS)
def test_get_free_tcp_port__checks_common_ports(port: int, monkeypatch):
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS if p is not port]

    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )
    assert get_free_tcp_port() is port


def test_get_free_tcp_port__checks_other_ports_if_common_ports_unavailable(monkeypatch):
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert get_free_tcp_port() is not None


def test_get_free_tcp_port__none_if_no_available_ports(monkeypatch):
    unavailable_ports = [Connection(("", p)) for p in range(65535)]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert get_free_tcp_port() is None
