import platform
import socket

from common import OperatingSystem


def get_os() -> OperatingSystem:
    """
    Get the OperatingSystem of the current execution environment.
    """
    # platform.system can return 'Linux', 'Windows', 'Darwin', 'Java'
    # or empty string if the value can't be determined
    system = platform.system()
    if system == "Windows":
        return OperatingSystem.WINDOWS
    elif system == "Linux":
        return OperatingSystem.LINUX
    elif system != "":
        return OperatingSystem.ANY
    raise RuntimeError(f"Agent is not supported on OS: '{system}'")


def get_os_version() -> str:
    return platform.platform()


def get_hostname():
    return socket.gethostname()
