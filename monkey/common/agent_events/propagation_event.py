from ipaddress import IPv4Address

from pydantic import Field

from . import AbstractAgentEvent


class PropagationEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent propagates on a host

    Attributes:
        :param target: IP address of the propagated system
        :param success: Status of the propagation
        :param exploiter_name: Name of the exploiter that propagated
        :param error_message: Message if an error occurs during propagation
    """

    target: IPv4Address
    success: bool
    exploiter_name: str
    error_message: str = Field(default="")
