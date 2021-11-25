import json
from logging import getLogger
from pathlib import Path

from common.utils.file_utils import expand_path
from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.cc.setup.island_config_options import IslandConfigOptions

logger = getLogger(__name__)


def get_server_config(island_args: IslandCmdArgs) -> IslandConfigOptions:
    config = IslandConfigOptions({})

    update_config_from_file(config, DEFAULT_SERVER_CONFIG_PATH)

    if island_args.server_config_path:
        path_to_config = expand_path(island_args.server_config_path)
        update_config_from_file(config, path_to_config)

    return config


def update_config_from_file(config: IslandConfigOptions, config_path: Path):
    try:
        config_from_file = load_server_config_from_file(config_path)
        config.update(config_from_file)
    except OSError:
        logger.info(f"Server config not found in path {config_path}")


def load_server_config_from_file(server_config_path) -> IslandConfigOptions:
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)
        return IslandConfigOptions(config)
