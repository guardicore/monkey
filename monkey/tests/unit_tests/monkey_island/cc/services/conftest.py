import pytest

from monkey_island.cc.environment import Environment
from monkey_island.cc.services.config import ConfigService


@pytest.fixture
def IPS():
    return ["0.0.0.0", "9.9.9.9"]


@pytest.fixture
def PORT():
    return 9999


@pytest.fixture
def config(monkeypatch, IPS, PORT):
    monkeypatch.setattr("monkey_island.cc.services.config.local_ip_addresses", lambda: IPS)
    monkeypatch.setattr(Environment, "_ISLAND_PORT", PORT)
    config = ConfigService.get_default_config(True)
    return config
