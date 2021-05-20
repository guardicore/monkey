import os

from monkey_island import config_file_parser
from monkey_island.cc.arg_parser import IslandArgs
from monkey_island.setup.setup_params import SetupParams


class SetupParamFactory:
    def __init__(self):
        self.setup_params = SetupParams()

    def build(self, cmd_args: IslandArgs, config_contents: dict) -> SetupParams:

        self._update_by_cmd_args(cmd_args)
        self._update_by_config_file(config_contents)

        return self.setup_params

    def _update_by_cmd_args(self, cmd_args: IslandArgs):
        if type(cmd_args.setup_only) == bool:
            self.setup_params.setup_only = cmd_args.setup_only

        if cmd_args.server_config_path:
            self.setup_params.server_config_path = os.path.expanduser(cmd_args.server_config_path)

    def _update_by_config_file(self, config_contents: dict):

        if "data_dir" in config_contents:
            self.setup_params.data_dir = config_contents["data_dir"]

        if "log_level" in config_contents:
            self.setup_params.log_level = config_contents["log_level"]

        if "mongodb" in config_contents and "start_mongodb" in config_contents["mongodb"]:
            self.setup_params.start_mongodb = config_contents["mongodb"]["start_mongodb"]
