import os
from pathlib import Path

from monkeytoolbox import get_os
from monkeytypes import OperatingSystem

from common.utils.file_utils import expand_path


def get_default_data_dir() -> str:
    if get_os() == OperatingSystem.WINDOWS:
        return r"%AppData%\monkey_island"
    else:
        return r"$HOME/.monkey_island"


# TODO: Figure out why windows requires the use of `os.getcwd()`. See issue #1207.
def _get_monkey_island_abs_path() -> str:
    if get_os() == OperatingSystem.WINDOWS:
        return os.path.join(os.getcwd(), "monkey_island")
    else:
        return str(Path(__file__).resolve().parent.parent.parent)


SERVER_CONFIG_FILENAME = "server_config.json"

MONKEY_ISLAND_ABS_PATH = _get_monkey_island_abs_path()

DEFAULT_DATA_DIR = expand_path(get_default_data_dir())

_MONGO_BINARY_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "mongodb")
_MONGO_EXECUTABLE_PATH_WIN = os.path.join(_MONGO_BINARY_DIR, "mongod.exe")
_MONGO_EXECUTABLE_PATH_LINUX = os.path.join(_MONGO_BINARY_DIR, "bin", "mongod")
MONGO_EXECUTABLE_PATH = (
    _MONGO_EXECUTABLE_PATH_WIN
    if get_os() == OperatingSystem.WINDOWS
    else _MONGO_EXECUTABLE_PATH_LINUX
)
MONGO_CONNECTION_TIMEOUT = 15

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_START_MONGO_DB = True

DEFAULT_CRT_PATH = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.crt"))
DEFAULT_KEY_PATH = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.key"))

GEVENT_EXCEPTION_LOG = "gevent_exceptions.log"

FLASK_PORT = 5000
