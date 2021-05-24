import os

from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR


def test_load_server_config_from_file(test_server_config, mock_home_env):
    config = server_config_handler.load_server_config_from_file(test_server_config)

    assert config["data_dir"] == os.path.join(mock_home_env, ".monkey_island")
    assert config["log_level"] == "NOTICE"


def test_default_log_level():
    test_config = {}
    config = server_config_handler.add_default_values_to_config(test_config)

    assert "log_level" in config
    assert config["log_level"] == "INFO"


def test_default_data_dir(mock_home_env):
    test_config = {}
    config = server_config_handler.add_default_values_to_config(test_config)

    assert "data_dir" in config
    assert config["data_dir"] == DEFAULT_DATA_DIR
