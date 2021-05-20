from monkey_island import config_file_parser
from monkey_island.cc.arg_parser import IslandArgs
from monkey_island.setup.setup_param_factory import SetupParamFactory

MOCK_ISLAND_CMD_ARGS = IslandArgs(setup_only=True, server_config_path="/temp/test_path")


def test_setup_param_factory_build(monkeypatch, test_server_config):
    config_contents = config_file_parser.load_server_config_from_file(test_server_config)

    setup_params = SetupParamFactory().build(MOCK_ISLAND_CMD_ARGS, config_contents)
    assert setup_params.setup_only
    assert setup_params.server_config_path == MOCK_ISLAND_CMD_ARGS.server_config_path
    assert setup_params.start_mongodb
    assert setup_params.log_level == "NOTICE"
    assert setup_params.data_dir == "~/.monkey_island"
