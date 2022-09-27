from pydantic import Field

from common.types import PingScanData

from . import AbstractAgentEvent


class PingScanEvent(AbstractAgentEvent):
    """
    An event that occurs when the agent performs a ping scan on its network

    Attributes:
        :param scan_data: The data collected from the ping scan
    """

    scan_data: PingScanData = Field(default=None)
