import os

__author__ = "itay.mizeretz"

MONKEY_ISLAND_ABS_PATH = os.path.join(os.getcwd(), "monkey_island")
DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS = 60 * 5

DEFAULT_SERVER_CONFIG_PATH = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "server_config.json")

DEFAULT_DEVELOP_SERVER_CONFIG_PATH = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", "server_config.json.develop"
)

DEFAULT_LOGGER_CONFIG_PATH = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", "island_logger_default_config.json"
)

DEFAULT_DATA_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc")
