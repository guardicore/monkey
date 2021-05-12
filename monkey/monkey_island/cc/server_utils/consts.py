import os

__author__ = "itay.mizeretz"

MONKEY_ISLAND_ABS_PATH = os.path.join(os.getcwd(), "monkey_island")

DEFAULT_DATA_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc")

DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS = 60 * 5

DEFAULT_SERVER_CONFIG_PATH = os.path.join(DEFAULT_DATA_DIR, "server_config.json")

DEFAULT_DEVELOP_SERVER_CONFIG_PATH = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", "server_config.json.develop"
)
