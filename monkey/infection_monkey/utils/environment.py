import platform
import sys
from socket import gethostname

from common import OperatingSystem


def get_os() -> OperatingSystem:
    """
    Get the OperatingSystem of the current execution environment.
    """
    system = platform.system()
    if system == "Windows":
        return OperatingSystem.WINDOWS
    if system == "Linux":
        return OperatingSystem.LINUX
    raise RuntimeError(f"Agent is not supported on OS: '{system}'")


def get_os_version() -> str:
    return platform.platform()


def is_windows_os():
    return sys.platform.startswith("win")


def get_hostname():
    return gethostname()
