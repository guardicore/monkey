import json
from logging import getLogger
from pathlib import Path

from common.utils.file_utils import expand_path
from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH, SERVER_CONFIG_FILENAME
from monkey_island.cc.setup.island_config_options import IslandConfigOptions

logger = getLogger(__name__)

PACKAGE_CONFIG_PATH = Path(MONKEY_ISLAND_ABS_PATH, "cc", SERVER_CONFIG_FILENAME)


def get_server_config(island_args: IslandCmdArgs) -> IslandConfigOptions:
    config = IslandConfigOptions()

    config = _update_config_from_file(config, PACKAGE_CONFIG_PATH)

    if island_args.server_config_path:
        path_to_config = expand_path(island_args.server_config_path)
        config = _update_config_from_file(config, path_to_config)

    return config


def _update_config_from_file(config: IslandConfigOptions, config_path: Path) -> IslandConfigOptions:
    try:
        config_from_file = _load_server_config_from_file(config_path)
        updated_config_dict = config.to_dict()
        updated_config_dict.update(config_from_file)
        updated_config = IslandConfigOptions(**updated_config_dict)
        logger.info(f"Server config updated from {config_path}")
        return updated_config
    except OSError:
        logger.warning(f"Server config not found in path {config_path}")
    return config


def _load_server_config_from_file(server_config_path) -> dict:
    with open(server_config_path, "r") as f:
        config_content = f.read()
        return json.loads(config_content)
