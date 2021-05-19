import os

from monkey_island import config_file_parser
from monkey_island.cc.arg_parser import IslandArgs
from monkey_island.setup.setup_params import SetupParams


class SetupParamFactory:
    @staticmethod
    def build(cmd_args: IslandArgs) -> SetupParams:

        setup_params = SetupParams()

        setup_params = SetupParamFactory._update_by_cmd_args(setup_params, cmd_args)
        setup_params = SetupParamFactory._update_by_config_file(setup_params)

        return setup_params

    @staticmethod
    def _update_by_cmd_args(setup_params: SetupParams, cmd_args: IslandArgs) -> SetupParams:
        if type(cmd_args.setup_only) == bool:
            setup_params.setup_only = cmd_args.setup_only

        if cmd_args.server_config_path:
            setup_params.server_config_path = os.path.expanduser(cmd_args.server_config_path)

        return setup_params

    @staticmethod
    def _update_by_config_file(setup_params: SetupParams):
        config = config_file_parser.load_server_config_from_file(setup_params.server_config_path)

        if "data_dir" in config:
            setup_params.data_dir = config["data_dir"]

        if "log_level" in config:
            setup_params.log_level = config["log_level"]

        if "mongodb" in config and "start_mongodb" in config["mongodb"]:
            setup_params.start_mongodb = config["mongodb"]["start_mongodb"]

        return setup_params
