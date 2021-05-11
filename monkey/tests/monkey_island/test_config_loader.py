import os

from monkey_island import config_loader


def test_load_server_config_from_file(test_server_config, mock_home_env):
    (data_dir, log_level) = config_loader.load_server_config(test_server_config)

    assert data_dir == os.path.join(mock_home_env, ".monkey_island")
    assert log_level == "NOTICE"
