from . import AbstractAgentEvent


class HostnameDiscoveryEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent identifies the hostname of the machine
    on which it is running

    Attributes:
        :param hostname: Hostname of the machine
    """

    hostname: str
