import pytest

from monkey_island.cc.services.config import ConfigService

# If tests fail because config path is changed, sync with
# monkey/monkey_island/cc/ui/src/components/pages/RunMonkeyPage/RunOptions.js


class MockClass:
    pass


@pytest.fixture(scope="function", autouse=True)
def mock_port_in_env_singleton(monkeypatch, PORT):
    mock_singleton = MockClass()
    mock_singleton.env = MockClass()
    mock_singleton.env.get_island_port = lambda: PORT
    monkeypatch.setattr("monkey_island.cc.services.config.env_singleton", mock_singleton)


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
