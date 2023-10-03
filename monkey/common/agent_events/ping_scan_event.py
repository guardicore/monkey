from ipaddress import IPv4Address
from typing import Optional

from monkeytypes import OperatingSystem

from . import AbstractAgentEvent


class PingScanEvent(AbstractAgentEvent):
    """
    An event that occurs when the agent performs a ping scan on its network

    Attributes:
        :param target: IP address of the pinged system
        :param response_received: Indicates if target responded to the ping
        :param os: Operating system type determined by ICMP fingerprinting
    """

    target: IPv4Address
    response_received: bool
    os: Optional[OperatingSystem]
