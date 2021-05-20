import sys


def is_windows_os() -> bool:
    return sys.platform.startswith("win")
