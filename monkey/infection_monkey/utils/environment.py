import platform
import socket

from monkeytypes import OperatingSystem


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


def get_hostname():
    return socket.gethostname()
