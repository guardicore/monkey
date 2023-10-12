from ipaddress import IPv4Address
from typing import Optional, Tuple

from monkeytypes import OperatingSystem
from pydantic import Field

from common.types import DiscoveredService

from . import AbstractAgentEvent


class FingerprintingEvent(AbstractAgentEvent):
    """
    An event that occurs when the agent performs a ping scan on its network

    Attributes:
        :param target: IP address of the pinged system
        :param os: Operating system determined during fingerprinting
        :param os_version: Operating system version determined during fingerprinting
        :param discovered_services: The services discovered and identified during fingerprinting
    """

    target: IPv4Address
    os: Optional[OperatingSystem] = Field(default=None)
    os_version: Optional[str] = Field(default=None)
    discovered_services: Tuple[DiscoveredService, ...] = Field(default_factory=tuple)
