from dataclasses import dataclass
from multiprocessing import Queue, get_context
from multiprocessing.context import BaseContext
from time import sleep
from typing import Tuple

import pytest

from infection_monkey.network.info import TCPPortSelector
from infection_monkey.network.ports import COMMON_PORTS

MULTIPROCESSING_PORT = 2222


@dataclass
class Connection:
    laddr: Tuple[str, int]


@pytest.fixture
def context() -> BaseContext:
    return get_context("spawn")


@pytest.fixture
def tcp_port_selector(context) -> TCPPortSelector:
    manager = context.Manager()
    return TCPPortSelector(context, manager)


@pytest.mark.parametrize("port", COMMON_PORTS)
def test_tcp_port_selector__checks_common_ports(
    tcp_port_selector: TCPPortSelector, port: int, monkeypatch
):
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS if p is not port]

    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )
    assert tcp_port_selector.get_free_tcp_port() is port


def test_tcp_port_selector__checks_other_ports_if_common_ports_unavailable(
    tcp_port_selector, monkeypatch
):
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert tcp_port_selector.get_free_tcp_port() is not None


def test_tcp_port_selector__none_if_no_available_ports(
    tcp_port_selector: TCPPortSelector, monkeypatch
):
    unavailable_ports = [Connection(("", p)) for p in range(65536)]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert tcp_port_selector.get_free_tcp_port() is None


@pytest.mark.parametrize("common_port", COMMON_PORTS)
def test_tcp_port_selector__checks_common_ports_leases(
    tcp_port_selector: TCPPortSelector, common_port: int, monkeypatch
):
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


def get_multiprocessing_tcp_port(
    tcp_port_selector: TCPPortSelector,
    port: int,
    queue: Queue,
    monkeypatch,
    lease_time_sec: float = 30.0,
):
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )
    free_tcp_port = tcp_port_selector.get_free_tcp_port(
        min_range=port, max_range=port, lease_time_sec=lease_time_sec
    )
    queue.put(free_tcp_port)


@pytest.mark.slow
def test_tcp_port_selector__uses_multiprocess_leases_same_random_port(
    tcp_port_selector: TCPPortSelector, context: BaseContext, monkeypatch
):

    queue = context.Queue()

    p1 = context.Process(
        target=get_multiprocessing_tcp_port,
        args=(tcp_port_selector, MULTIPROCESSING_PORT, queue, monkeypatch),
    )
    p2 = context.Process(
        target=get_multiprocessing_tcp_port,
        args=(tcp_port_selector, MULTIPROCESSING_PORT, queue, monkeypatch),
    )
    p1.start()
    p2.start()
    free_tcp_port_1 = queue.get()
    free_tcp_port_2 = queue.get()
    p1.join()
    p2.join()

    actual_results = [free_tcp_port_1, free_tcp_port_2]

    assert MULTIPROCESSING_PORT in actual_results
    assert None in actual_results


@pytest.mark.slow
def test_tcp_port_selector__uses_multiprocess_leases(
    tcp_port_selector: TCPPortSelector, context: BaseContext, monkeypatch
):
    queue = context.Queue()

    p1 = context.Process(
        target=get_multiprocessing_tcp_port,
        args=(tcp_port_selector, MULTIPROCESSING_PORT, queue, monkeypatch, 0.0001),
    )
    p1.start()
    sleep(0.0001)
    free_tcp_port_1 = queue.get()
    p1.join()

    p2 = context.Process(
        target=get_multiprocessing_tcp_port,
        args=(tcp_port_selector, MULTIPROCESSING_PORT, queue, monkeypatch),
    )
    p2.start()
    free_tcp_port_2 = queue.get()
    p2.join()

    assert MULTIPROCESSING_PORT == free_tcp_port_1
    assert MULTIPROCESSING_PORT == free_tcp_port_2
