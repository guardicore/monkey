from enum import Enum

from . import AbstractAgentEvent


class DefacementEvent(AbstractAgentEvent):
    """
    An event that occurs when an attacker modifies some visual content or component

    Attributes:
        :param defacement_target: Whether the defacement is internally or externally targeted
        :param description: A description of the defacement
    """

    class DefacementTarget(Enum):
        INTERNAL = "internal"
        EXTERNAL = "external"

    defacement_target: DefacementTarget
    description: str
