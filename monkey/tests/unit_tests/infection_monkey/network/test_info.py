from dataclasses import dataclass
from multiprocessing import Queue, get_context
from multiprocessing.context import BaseContext
from multiprocessing.managers import SyncManager
from random import SystemRandom
from time import sleep
from typing import Tuple

import pytest

from common.types import NetworkPort
from infection_monkey.network import TCPPortSelector
from infection_monkey.network.ports import COMMON_PORTS

MULTIPROCESSING_PORT = 2222
RANDOM_PORTS_NUMBER = 3


@dataclass
class Connection:
    laddr: Tuple[str, int]


@pytest.fixture
def context() -> BaseContext:
    return get_context("spawn")


@pytest.fixture
def tcp_port_selector() -> TCPPortSelector:
    return TCPPortSelector()


class MonkeyPatch:
    def __init__(self, monkeypatch):
        self.monkeypatch = monkeypatch

    def setattr(self, *args, **kwargs):
        self.monkeypatch.setattr(*args, **kwargs)


def unavailable_ports():
    return [Connection(("", p)) for p in COMMON_PORTS]


@pytest.fixture
def multiprocessing_tcp_port_selector(context: BaseContext, monkeypatch) -> TCPPortSelector:
    # Registering TCPPortSelector as a proxy object, making it multiprocessing-safe
    # Registering the MonkeyPatch class in order to execute monkeypatch.setattr on the managed
    # process
    SyncManager.register("TCPPortSelector", TCPPortSelector)
    SyncManager.register("MonkeyPatch", MonkeyPatch)
    manager = context.Manager()
    monkeypatch_proxy = manager.MonkeyPatch(monkeypatch)  # type: ignore[attr-defined]
    monkeypatch_proxy.setattr(
        "infection_monkey.network.info.psutil.net_connections", unavailable_ports
    )
    return manager.TCPPortSelector()  # type: ignore[attr-defined]


def test_tcp_port_selector__checks_preferred_ports(tcp_port_selector: TCPPortSelector, monkeypatch):
    preferred_ports = [NetworkPort(1111), NetworkPort(2222), NetworkPort(3333)]
    preferred_port = SystemRandom().choice(preferred_ports)
    unavailable_ports = [Connection(("", p)) for p in preferred_ports if p is not preferred_port]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )
    assert tcp_port_selector.get_free_tcp_port(preferred_ports=preferred_ports) in preferred_ports


@pytest.mark.slow
@pytest.mark.parametrize("number_of_runs", range(RANDOM_PORTS_NUMBER))
def test_tcp_port_selector__checks_common_ports(
    tcp_port_selector: TCPPortSelector, number_of_runs: int, monkeypatch
):
    common_port = SystemRandom().choice(COMMON_PORTS)
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS if p is not common_port]

    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )
    assert tcp_port_selector.get_free_tcp_port() is common_port


@pytest.mark.slow
def test_tcp_port_selector__checks_other_ports_if_common_ports_unavailable(
    tcp_port_selector, monkeypatch
):
    unavailable_ports = [Connection(("", p)) for p in COMMON_PORTS]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert tcp_port_selector.get_free_tcp_port() not in COMMON_PORTS


@pytest.mark.slow
def test_tcp_port_selector__none_if_no_available_ports(
    tcp_port_selector: TCPPortSelector, monkeypatch
):
    unavailable_ports = [Connection(("", p)) for p in range(65536)]
    monkeypatch.setattr(
        "infection_monkey.network.info.psutil.net_connections", lambda: unavailable_ports
    )

    assert tcp_port_selector.get_free_tcp_port() is None


@pytest.mark.slow
@pytest.mark.parametrize("number_of_runs", range(RANDOM_PORTS_NUMBER))
def test_tcp_port_selector__checks_common_ports_leases(
    tcp_port_selector: TCPPortSelector, number_of_runs: int, monkeypatch
):
    common_port = SystemRandom().choice(COMMON_PORTS)
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
    lease_time_sec: float = 30.0,
):
    free_tcp_port = tcp_port_selector.get_free_tcp_port(
        min_range=port, max_range=port, lease_time_sec=lease_time_sec
    )
    queue.put(free_tcp_port)


@pytest.mark.slow
def test_tcp_port_selector__uses_multiprocess_leases_same_random_port(
    multiprocessing_tcp_port_selector: TCPPortSelector, context: BaseContext
):
    queue = context.Queue()

    p1 = context.Process(  # type: ignore[attr-defined]
        target=get_multiprocessing_tcp_port,
        args=(multiprocessing_tcp_port_selector, MULTIPROCESSING_PORT, queue),
    )
    p2 = context.Process(  # type: ignore[attr-defined]
        target=get_multiprocessing_tcp_port,
        args=(multiprocessing_tcp_port_selector, MULTIPROCESSING_PORT, queue),
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
    multiprocessing_tcp_port_selector: TCPPortSelector, context: BaseContext
):
    queue = context.Queue()

    p1 = context.Process(  # type: ignore[attr-defined]
        target=get_multiprocessing_tcp_port,
        args=(multiprocessing_tcp_port_selector, MULTIPROCESSING_PORT, queue, 0.0001),
    )
    p1.start()
    sleep(0.0001)
    free_tcp_port_1 = queue.get()
    p1.join()

    p2 = context.Process(  # type: ignore[attr-defined]
        target=get_multiprocessing_tcp_port,
        args=(multiprocessing_tcp_port_selector, MULTIPROCESSING_PORT, queue),
    )
    p2.start()
    free_tcp_port_2 = queue.get()
    p2.join()

    assert MULTIPROCESSING_PORT == free_tcp_port_1
    assert MULTIPROCESSING_PORT == free_tcp_port_2
