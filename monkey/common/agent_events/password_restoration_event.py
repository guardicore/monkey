from ipaddress import IPv4Address

from . import AbstractAgentEvent


class PasswordRestorationEvent(AbstractAgentEvent):
    """
    An event that occurs when a password has been restored on the target
    system

    Attributes:
        :param target: The IP of the target system on which the
            restoration was performed
        :param success: If the password restoration was successful
    """

    target: IPv4Address
    success: bool
