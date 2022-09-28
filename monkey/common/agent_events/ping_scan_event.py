from typing import Optional

from common import OperatingSystem

from . import AbstractAgentEvent


class PingScanEvent(AbstractAgentEvent):
    """
    An event that occurs when the agent performs a ping scan on its network

    Attributes:
        :param response_received: Is any response from ping recieved
        :param os: Operating system from the target system
    """

    response_received: bool
    os: Optional[OperatingSystem]
