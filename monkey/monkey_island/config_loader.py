import json
import os

from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR

DEFAULT_LOG_LEVEL = "INFO"


def load_server_config(server_config_path):
    with open(server_config_path, "r") as f:
        config_content = f.read()
        data = json.loads(config_content)
        data_dir = os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(data["data_dir"] if "data_dir" in data else DEFAULT_DATA_DIR)
            )
        )
        log_level = data["log_level"] if "log_level" in data else DEFAULT_LOG_LEVEL

        return data_dir, log_level
