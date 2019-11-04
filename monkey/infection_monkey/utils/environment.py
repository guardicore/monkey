import os
import struct
import sys
import enum
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


class OperatingSystems(enum):
    WINDOWS = "windows"
    LINUX = "linux"


class Distribution:
    def __init__(self, operating_system: OperatingSystems, distribution: str):
        self.operating_system = operating_system
        self.distribution = distribution

    def is_on_current_system(self):
        system_platform = platform.platform().toLower()
        return self.operating_system in system_platform and self.distribution in system_platform
