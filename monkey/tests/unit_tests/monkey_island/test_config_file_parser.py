from monkey_island import config_file_parser
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR, DEFAULT_LOG_LEVEL


def test_load_server_config_from_file(server_config_init_only):
    config = config_file_parser.load_island_config_from_file(server_config_init_only)

    assert config.data_dir == "~/.monkey_island"
    assert config.log_level == "NOTICE"


def test_load_server_config_from_file_empty_file(monkeypatch, server_config_empty):
    config = config_file_parser.load_island_config_from_file(server_config_empty)

    assert config.data_dir == DEFAULT_DATA_DIR
    assert config.log_level == DEFAULT_LOG_LEVEL
