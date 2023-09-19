from pydantic import conint

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
    bytes: conint(ge=0, strict=True)  # type: ignore [valid-type]
