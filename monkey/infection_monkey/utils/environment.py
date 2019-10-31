import os
import struct
import sys


def is_64bit_windows_os():
    """
    Checks for 64 bit Windows OS using environment variables.
    """
    return 'PROGRAMFILES(X86)' in os.environ


def is_64bit_python():
    return struct.calcsize("P") == 8


def is_windows_os():
    return sys.platform.startswith("win")
