from enum import Enum, auto


class AccountRole(Enum):
    """
    An Enum representing  roles.
    This Enum represents roles that an account can have.
    """

    ISLAND_INTERFACE = auto()
    AGENT = auto()
