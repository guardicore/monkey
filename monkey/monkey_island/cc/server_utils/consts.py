import os
from pathlib import Path

from common.utils.environment import is_windows_os
from common.utils.file_utils import expand_path


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
UI_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "next_ui")

DEFAULT_DATA_DIR = expand_path(get_default_data_dir())

_MONGO_BINARY_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "mongodb")
_MONGO_EXECUTABLE_PATH_WIN = os.path.join(_MONGO_BINARY_DIR, "mongod.exe")
_MONGO_EXECUTABLE_PATH_LINUX = os.path.join(_MONGO_BINARY_DIR, "bin", "mongod")
MONGO_EXECUTABLE_PATH = (
    _MONGO_EXECUTABLE_PATH_WIN if is_windows_os() else _MONGO_EXECUTABLE_PATH_LINUX
)
MONGO_CONNECTION_TIMEOUT = 15

_NODE_EXECUTABLE_PATH_WIN = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "node", "node.exe")
_NODE_EXECUTABLE_PATH_LINUX = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "node", "node")
NODE_EXECUTABLE_PATH = _NODE_EXECUTABLE_PATH_WIN if is_windows_os() else _NODE_EXECUTABLE_PATH_LINUX
NEXTJS_EXECUTION_COMMAND = [NODE_EXECUTABLE_PATH, "server.js"]

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_START_MONGO_DB = True

DEFAULT_CRT_PATH = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.crt"))
DEFAULT_KEY_PATH = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.key"))

DEFAULT_JAVASCRIPT_RUNTIME_PORT = 443

GEVENT_EXCEPTION_LOG = "gevent_exceptions.log"

ISLAND_PORT = 5000
