import os
import struct
import sys
from enum import Enum
import platform


def is_64bit_windows_os():
    """
    Checks for 64 bit Windows OS using environment variables.
    """
    return 'PROGRAMFILES(X86)' in os.environ


def is_64bit_python():
    return struct.calcsize("P") == 8


def is_windows_os():
    return sys.platform.startswith("win")


class OperatingSystemTypes(Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class OperatingSystemVersion(Enum):
    UBUNTU = "ubuntu"


class OperatingSystem:
    def __init__(self, operating_system: OperatingSystemTypes, version: OperatingSystemVersion):
        self.operating_system = operating_system.value
        self.version = version.value

    def is_on_current_system(self):
        system_platform = platform.platform().lower()
        return self.operating_system in system_platform and self.version in system_platform
