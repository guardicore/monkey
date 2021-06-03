import os
from pathlib import Path

from monkey_island.cc.environment.utils import is_windows_os

__author__ = "itay.mizeretz"


def get_default_data_dir() -> str:
    if is_windows_os():
        return r"%AppData%\monkey_island"
    else:
        return r"$HOME/.monkey_island"


# TODO: Figure out why windows requires the use of `os.getcwd()`. See issue #1207.
def _get_monkey_island_abs_path() -> str:
    if is_windows_os():
        return os.path.join(os.getcwd(), "monkey_island")
    else:
        return str(Path(__file__).resolve().parent.parent.parent)


SERVER_CONFIG_FILENAME = "server_config.json"

MONKEY_ISLAND_ABS_PATH = _get_monkey_island_abs_path()

DEFAULT_DATA_DIR = os.path.expandvars(get_default_data_dir())

DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS = 60 * 5

_MONGO_BINARY_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "mongodb")
_MONGO_EXECUTABLE_PATH_WIN = os.path.join(_MONGO_BINARY_DIR, "mongod.exe")
_MONGO_EXECUTABLE_PATH_LINUX = os.path.join(_MONGO_BINARY_DIR, "bin", "mongod")
MONGO_EXECUTABLE_PATH = (
    _MONGO_EXECUTABLE_PATH_WIN if is_windows_os() else _MONGO_EXECUTABLE_PATH_LINUX
)

DEFAULT_SERVER_CONFIG_PATH = os.path.expandvars(
    os.path.join(DEFAULT_DATA_DIR, SERVER_CONFIG_FILENAME)
)

DEFAULT_DEVELOP_SERVER_CONFIG_PATH = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", f"{SERVER_CONFIG_FILENAME}.develop"
)

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_START_MONGO_DB = True
