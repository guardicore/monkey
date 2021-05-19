from dataclasses import dataclass

from monkey_island.cc.server_utils.consts import (
    DEFAULT_DATA_DIR,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SERVER_CONFIG_PATH,
    DEFAULT_SHOULD_SETUP_ONLY,
    DEFAULT_START_MONGO_DB,
)


@dataclass
class SetupParams:
    server_config_path = DEFAULT_SERVER_CONFIG_PATH
    log_level = DEFAULT_LOG_LEVEL
    data_dir = DEFAULT_DATA_DIR
    start_mongodb = DEFAULT_START_MONGO_DB
    setup_only = DEFAULT_SHOULD_SETUP_ONLY
