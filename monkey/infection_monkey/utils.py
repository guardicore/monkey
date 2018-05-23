import os
import sys
import struct

from config import WormConfiguration


def get_monkey_log_path():
    return os.path.expandvars(WormConfiguration.monkey_log_path_windows) if sys.platform == "win32" \
        else WormConfiguration.monkey_log_path_linux


def get_dropper_log_path():
    return os.path.expandvars(WormConfiguration.dropper_log_path_windows) if sys.platform == "win32" \
        else WormConfiguration.dropper_log_path_linux


def is_64bit_windows_os():
    '''
    Checks for 64 bit Windows OS using environment variables.
    :return:
    '''
    return 'PROGRAMFILES(X86)' in os.environ


def is_64bit_python():
    return struct.calcsize("P") == 8


def is_windows_os():
    return sys.platform.startswith("win")
