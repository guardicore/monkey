import json
import os

from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR

DEFAULT_LOG_LEVEL = "INFO"


def load_server_config(server_config_path):
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)
        config["data_dir"] = os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(config["data_dir"] if "data_dir" in config else DEFAULT_DATA_DIR)
            )
        )
        config["log_level"] = config["log_level"] if "log_level" in config else DEFAULT_LOG_LEVEL

        return config
