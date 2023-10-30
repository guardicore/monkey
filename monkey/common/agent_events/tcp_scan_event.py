from ipaddress import IPv4Address
from typing import Dict

from monkeytypes import PortStatus

from common.types import NetworkPort

from . import AbstractAgentEvent


class TCPScanEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent performs a TCP scan on a host

    Attributes:
        :param target: IP address of the scanned system
        :param ports: The scanned ports and their status (open/closed)
    """

    target: IPv4Address
    ports: Dict[NetworkPort, PortStatus]
