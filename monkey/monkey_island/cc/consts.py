import os

__author__ = 'itay.mizeretz'

MONKEY_ISLAND_ABS_PATH = os.path.join(os.getcwd(), 'monkey_island')
DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS = 60 * 5

_SERVER_CONFIG_FILENAME = "server_config.json"
DEFAULT_SERVER_CONFIG_PATH = os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', _SERVER_CONFIG_FILENAME)
