from monkeytypes import OperatingSystem

from . import AbstractAgentEvent


class OSDiscoveryEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent identifies the OS of the machine
    on which it is running.

    Attributes:
        :param os: Operating system type
        :param version: OS-specific version string
    """

    os: OperatingSystem
    version: str
