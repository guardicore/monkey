from enum import Enum


class OperatingSystem(Enum):
    """
    An Enum representing all supported operating systems

    This Enum represents all operating systems that Infection Monkey supports. The value of each
    member is the member's name in all lower-case characters.
    """

    LINUX = "linux"
    WINDOWS = "windows"
