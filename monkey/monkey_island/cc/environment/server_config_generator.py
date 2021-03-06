from pathlib import Path

from monkey_island.cc.server_utils.consts import DEFAULT_DEVELOP_SERVER_CONFIG_PATH


def create_default_config_file(path):
    default_config = Path(DEFAULT_DEVELOP_SERVER_CONFIG_PATH).read_text()
    Path(path).write_text(default_config)
