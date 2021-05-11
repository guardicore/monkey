import os

from monkey_island import config_loader


def test_load_server_config_from_file(test_server_config, mock_home_env):
    config = config_loader.load_server_config(test_server_config)

    assert config["data_dir"] == os.path.join(mock_home_env, ".monkey_island")
    assert config["log_level"] == "NOTICE"
