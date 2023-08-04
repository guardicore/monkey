import pytest
from agent_plugins.payloads.cryptominer.src.cryptominer_options import CryptominerOptions

CRYPTOMINER_OPTIONS_DICT = {
    "simulation_time": 100,
    "cpu_utilization": 50,
    "memory_utilization": 30,
    "send_dummy_request": True,
}

CRYPTOMINER_OPTIONS_OBJECT = CryptominerOptions(
    simulation_time=100,
    cpu_utilization=50,
    memory_utilization=30,
    send_dummy_request=True,
)


def test_cryptominer_options__serialization():
    assert CRYPTOMINER_OPTIONS_OBJECT.dict(simplify=True) == CRYPTOMINER_OPTIONS_DICT


def test_cryptominer_options__full_serialization():
    assert (
        CryptominerOptions(**CRYPTOMINER_OPTIONS_OBJECT.dict(simplify=True))
        == CRYPTOMINER_OPTIONS_OBJECT
    )


def test_cryptominer_options__deserialization():
    assert CryptominerOptions(**CRYPTOMINER_OPTIONS_DICT) == CRYPTOMINER_OPTIONS_OBJECT


def test_cryptominer_options__default():
    cryptominer_options = CryptominerOptions()

    assert cryptominer_options.simulation_time == 300
    assert cryptominer_options.cpu_utilization == 20
    assert cryptominer_options.memory_utilization == 20
    assert cryptominer_options.send_dummy_request is False


def test_cryptominer_options__invalid_simulation_time():
    with pytest.raises(ValueError):
        CryptominerOptions(simulation_time=-123)


@pytest.mark.parametrize("cpu_utilization", ["-1", "101"])
def test_cryptominer_options__invalid_cpu_utilization(cpu_utilization: int):
    with pytest.raises(ValueError):
        CryptominerOptions(cpu_utilization=cpu_utilization)


@pytest.mark.parametrize("memory_utilization", ["-1", "101"])
def test_cryptominer_options__invalid_memory_utilization(memory_utilization: int):
    with pytest.raises(ValueError):
        CryptominerOptions(memory_utilization=memory_utilization)
