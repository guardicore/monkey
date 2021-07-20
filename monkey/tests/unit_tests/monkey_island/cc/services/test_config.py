import pytest

from monkey_island.cc.environment import Environment
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

IPS = ["0.0.0.0", "9.9.9.9"]
PORT = 9999


# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.local_ip_addresses", lambda: IPS)
    monkeypatch.setattr(Environment, "_ISLAND_PORT", PORT)
    config = ConfigService.get_default_config(True)
    return config


class MockClass:
    pass


@pytest.fixture(scope="function", autouse=True)
def mock_port_in_env_singleton(monkeypatch):
    mock_singleton = MockClass()
    mock_singleton.env = MockClass()
    mock_singleton.env.get_island_port = lambda: PORT
    monkeypatch.setattr("monkey_island.cc.services.config.env_singleton", mock_singleton)


def test_set_server_ips_in_config_command_servers(config):
    ConfigService.set_server_ips_in_config(config)
    expected_config_command_servers = [f"{ip}:{PORT}" for ip in IPS]
    assert config["internal"]["island_server"]["command_servers"] == expected_config_command_servers


def test_set_server_ips_in_config_current_server(config):
    ConfigService.set_server_ips_in_config(config)
    expected_config_current_server = f"{IPS[0]}:{PORT}"
    assert config["internal"]["island_server"]["current_server"] == expected_config_current_server


def test_update_config_on_mode_set_advanced(config, monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.ConfigService.get_config", lambda: config)
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.update_config",
        lambda config_json, should_encrypt: config_json,
    )

    mode = IslandModeEnum.ADVANCED
    manipulated_config = ConfigService.update_config_on_mode_set(mode)
    assert manipulated_config == config


def test_update_config_on_mode_set_ransomware(config, monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.ConfigService.get_config", lambda: config)
    monkeypatch.setattr(
        "monkey_island.cc.services.config.ConfigService.update_config",
        lambda config_json, should_encrypt: config_json,
    )

    mode = IslandModeEnum.RANSOMWARE
    manipulated_config = ConfigService.update_config_on_mode_set(mode)
    assert manipulated_config["monkey"]["post_breach"]["post_breach_actions"] == []
