import pytest
from agent_plugins.payloads.cryptojacker.src.cryptojacker_options import CryptojackerOptions

CRYPTOJACKER_OPTIONS_DICT = {
    "duration": 100,
    "cpu_utilization": 50,
    "memory_utilization": 30,
    "simulate_bitcoin_mining_network_traffic": True,
}

CRYPTOJACKER_OPTIONS_OBJECT = CryptojackerOptions(
    duration=100,
    cpu_utilization=50,
    memory_utilization=30,
    simulate_bitcoin_mining_network_traffic=True,
)


def test_cryptojacker_options__serialization():
    assert CRYPTOJACKER_OPTIONS_OBJECT.dict(simplify=True) == CRYPTOJACKER_OPTIONS_DICT


def test_cryptojacker_options__full_serialization():
    assert (
        CryptojackerOptions(**CRYPTOJACKER_OPTIONS_OBJECT.dict(simplify=True))
        == CRYPTOJACKER_OPTIONS_OBJECT
    )


def test_cryptojacker_options__deserialization():
    assert CryptojackerOptions(**CRYPTOJACKER_OPTIONS_DICT) == CRYPTOJACKER_OPTIONS_OBJECT


def test_cryptojacker_options__default():
    cryptojacker_options = CryptojackerOptions()

    assert cryptojacker_options.duration == 300
    assert cryptojacker_options.cpu_utilization == 80
    assert cryptojacker_options.memory_utilization == 20
    assert cryptojacker_options.simulate_bitcoin_mining_network_traffic is False


def test_cryptojacker_options__invalid_duration():
    with pytest.raises(ValueError):
        CryptojackerOptions(duration=-123)


@pytest.mark.parametrize("cpu_utilization", ["-1", "101"])
def test_cryptojacker_options__invalid_cpu_utilization(cpu_utilization: int):
    with pytest.raises(ValueError):
        CryptojackerOptions(cpu_utilization=cpu_utilization)


@pytest.mark.parametrize("memory_utilization", ["-1", "101"])
def test_cryptojacker_options__invalid_memory_utilization(memory_utilization: int):
    with pytest.raises(ValueError):
        CryptojackerOptions(memory_utilization=memory_utilization)
