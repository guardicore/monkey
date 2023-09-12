from enum import Enum

from . import AbstractAgentEvent


class DefacementEvent(AbstractAgentEvent):
    """
    An event that occurs when an attacker modifies some visual content or component

    Attributes:
        :param visibility: Whether the defacement is internally or externally visible
        :param description: A description of the defacement
    """

    class DefacementVisibility(Enum):
        INTERNAL = "internal"
        EXTERNAL = "external"

    visibility: DefacementVisibility
    description: str
