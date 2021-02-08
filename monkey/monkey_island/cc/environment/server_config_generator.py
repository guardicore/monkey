from pathlib import Path

from monkey_island.cc.consts import DEFAULT_STANDARD_SERVER_CONFIG


def create_default_config_file(path):
    default_config = Path(DEFAULT_STANDARD_SERVER_CONFIG).read_text()
    Path(path).write_text(default_config)
