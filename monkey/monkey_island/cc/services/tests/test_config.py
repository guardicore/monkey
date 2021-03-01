import pytest

import monkey_island.cc.services.config
from monkey_island.cc.environment import Environment
from monkey_island.cc.services.config import ConfigService

IPS = ["0.0.0.0", "9.9.9.9"]
PORT = 9999

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.local_ip_addresses",
                        lambda: IPS)
    monkeypatch.setattr(Environment, "_ISLAND_PORT", PORT)
    config = ConfigService.get_default_config(True)
    return config


def test_set_server_ips_in_config_command_servers(config):
    ConfigService.set_server_ips_in_config(config)
    expected_config_command_servers = [f"{ip}:{PORT}" for ip in IPS]
    assert config["internal"]["island_server"]["command_servers"] ==\
        expected_config_command_servers


def test_set_server_ips_in_config_current_server(config):
    ConfigService.set_server_ips_in_config(config)
    expected_config_current_server = f"{IPS[0]}:{PORT}"
    assert config["internal"]["island_server"]["current_server"] ==\
        expected_config_current_server
