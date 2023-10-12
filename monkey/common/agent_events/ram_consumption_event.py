from pydantic import Field
from typing_extensions import Annotated

from common.types import Percent

from . import AbstractAgentEvent


class RAMConsumptionEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent consumes significant RAM for its own purposes.

    Attributes:
        :param utilization: The percentage of the RAM is utilized
        :param bytes: The number of bytes of RAM that are utilized
    """

    utilization: Percent
    bytes: Annotated[int, Field(ge=0, strict=True)]
