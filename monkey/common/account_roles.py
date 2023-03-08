from enum import Enum


class AccountRoles(Enum):
    """
    An Enum representing user roles.
    This Enum represents roles that the user can have. The value
    of each member is the description of the role
    """

    ISLAND = "Monkey Island, C&C Server"
    AGENT = "Infection Monkey Agent"
