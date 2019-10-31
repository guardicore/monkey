import os
import sys

from infection_monkey.config import WormConfiguration


def get_monkey_log_path():
    return os.path.expandvars(WormConfiguration.monkey_log_path_windows) if sys.platform == "win32" \
        else WormConfiguration.monkey_log_path_linux


def get_dropper_log_path():
    return os.path.expandvars(WormConfiguration.dropper_log_path_windows) if sys.platform == "win32" \
        else WormConfiguration.dropper_log_path_linux
