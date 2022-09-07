import pytest

from infection_monkey.model import VictimHostFactory
from infection_monkey.network import NetworkAddress


@pytest.fixture(autouse=True)
def mock_get_interface_to_target(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.model.victim_host_factory.get_interface_to_target", lambda _: "1.1.1.1"
    )


def test_factory_no_tunnel():
    factory = VictimHostFactory(island_ip="192.168.56.1", island_port="5000", on_island=False)
    network_address = NetworkAddress("192.168.56.2", None)

    victim = factory.build_victim_host(network_address)

    assert victim.default_server == "192.168.56.1:5000"
    assert victim.ip_addr == "192.168.56.2"
    assert victim.default_tunnel is None
    assert victim.domain_name == ""


def test_factory_on_island():
    factory = VictimHostFactory(island_ip="192.168.56.1", island_port="99", on_island=True)
    network_address = NetworkAddress("192.168.56.2", "www.bogus.monkey")

    victim = factory.build_victim_host(network_address)

    assert victim.default_server == "1.1.1.1:99"
    assert victim.domain_name == "www.bogus.monkey"
    assert victim.ip_addr == "192.168.56.2"
    assert victim.default_tunnel == "1.2.3.4:1234"


@pytest.mark.parametrize("default_port", ["", None])
def test_factory_no_port(default_port):
    factory = VictimHostFactory(island_ip="192.168.56.1", island_port=default_port, on_island=True)
    network_address = NetworkAddress("192.168.56.2", "www.bogus.monkey")

    victim = factory.build_victim_host(network_address)

    assert victim.default_server == "1.1.1.1"


def test_factory_no_default_server():
    factory = VictimHostFactory(island_ip=None, island_port="", on_island=True)
    network_address = NetworkAddress("192.168.56.2", "www.bogus.monkey")

    victim = factory.build_victim_host(network_address)

    assert victim.default_server is None
