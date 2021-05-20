from monkey_island import config_file_parser


def test_load_server_config_from_file(test_server_config):
    config = config_file_parser.load_server_config_from_file(test_server_config)

    assert config["data_dir"] == "~/.monkey_island"
    assert config["log_level"] == "NOTICE"


def test_load_server_config_from_file_default_path(monkeypatch, test_server_config):
    monkeypatch.setattr(config_file_parser, "DEFAULT_SERVER_CONFIG_PATH", test_server_config)
    config = config_file_parser.load_server_config_from_file("")

    assert config["data_dir"] == "~/.monkey_island"
    assert config["log_level"] == "NOTICE"
