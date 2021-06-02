from __future__ import annotations

import os

from monkey_island.cc.server_utils.consts import (
    DEFAULT_CRT_PATH,
    DEFAULT_DATA_DIR,
    DEFAULT_KEY_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)


class IslandConfigOptions:
    def __init__(self, config_contents: dict):
        self.data_dir = os.path.expandvars(
            os.path.expanduser(config_contents.get("data_dir", DEFAULT_DATA_DIR))
        )

        self.log_level = config_contents.get("log_level", DEFAULT_LOG_LEVEL)

        self.start_mongodb = config_contents.get(
            "mongodb", {"start_mongodb": DEFAULT_START_MONGO_DB}
        ).get("start_mongodb", DEFAULT_START_MONGO_DB)

        self.crt_path = config_contents.get("cert_path", DEFAULT_CRT_PATH)
        self.key_path = config_contents.get("cert_path", DEFAULT_KEY_PATH)
