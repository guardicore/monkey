import os

__author__ = "itay.mizeretz"

MONKEY_ISLAND_ABS_PATH = os.path.join(os.getcwd(), "monkey_island")
DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS = 60 * 5

# TODO move setup consts
DEFAULT_SERVER_CONFIG_PATH = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "server_config.json")

DEFAULT_DEVELOP_SERVER_CONFIG_PATH = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", "server_config.json.develop"
)

DEFAULT_DATA_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc")
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_START_MONGO_DB = True
DEFAULT_SHOULD_SETUP_ONLY = False
