from __future__ import annotations

from dataclasses import dataclass

from monkey_island.cc.server_utils.consts import (
    DEFAULT_DATA_DIR,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)


@dataclass
class IslandConfigOptions:
    log_level = DEFAULT_LOG_LEVEL
    data_dir = DEFAULT_DATA_DIR
    start_mongodb = DEFAULT_START_MONGO_DB

    @staticmethod
    def build_from_config_file_contents(config_contents: dict) -> IslandConfigOptions:
        config = IslandConfigOptions()
        if "data_dir" in config_contents:
            config.data_dir = config_contents["data_dir"]

        if "log_level" in config_contents:
            config.log_level = config_contents["log_level"]

        if "mongodb" in config_contents and "start_mongodb" in config_contents["mongodb"]:
            config.start_mongodb = config_contents["mongodb"]["start_mongodb"]

        return config
