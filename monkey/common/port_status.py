from enum import Enum


class PortStatus(Enum):
    """
    An Enum representing the status of the port.

    This Enum represents the status of a network pork. The value of each
    member is distincive and unique number.
    """

    OPEN = 1
    CLOSED = 2
