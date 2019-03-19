import os
import sys
import shutil
import struct

from infection_monkey.config import WormConfiguration


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


def utf_to_ascii(string):
    # Converts utf string to ascii. Safe to use even if string is already ascii.
    udata = string.decode("utf-8")
    return udata.encode("ascii", "ignore")


def create_monkey_dir():
    """
    Creates directory for monkey and related files
    """
    if is_windows_os():
        if not os.path.exists(WormConfiguration.monkey_dir_windows):
            os.mkdir(WormConfiguration.monkey_dir_windows)
    else:
        if not os.path.exists(WormConfiguration.monkey_log_path_linux):
            os.mkdir(WormConfiguration.monkey_dir_linux)


def remove_monkey_dir():
    """
    Removes monkey's root directory
    """
    if is_windows_os():
        shutil.rmtree(WormConfiguration.monkey_dir_windows, ignore_errors=True)
    else:
        shutil.rmtree(WormConfiguration.monkey_dir_linux, ignore_errors=True)
