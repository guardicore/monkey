import pytest

from monkey_island.cc.services.config import ConfigService

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


class MockClass:
    pass


@pytest.fixture(scope="function", autouse=True)
def mock_port(monkeypatch, PORT):
    monkeypatch.setattr("monkey_island.cc.services.config.ISLAND_PORT", PORT)


@pytest.mark.usefixtures("uses_encryptor")
def test_set_server_ips_in_config_command_servers(config, IPS, PORT):
    ConfigService.set_server_ips_in_config(config)
    expected_config_command_servers = [f"{ip}:{PORT}" for ip in IPS]
    assert config["internal"]["island_server"]["command_servers"] == expected_config_command_servers


@pytest.mark.usefixtures("uses_encryptor")
def test_set_server_ips_in_config_current_server(config, IPS, PORT):
    ConfigService.set_server_ips_in_config(config)
    expected_config_current_server = f"{IPS[0]}:{PORT}"
    assert config["internal"]["island_server"]["current_server"] == expected_config_current_server
