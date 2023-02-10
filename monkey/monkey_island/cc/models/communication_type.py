from enum import Enum


class CommunicationType(Enum):
    """
    An Enum representing different types of communication between agents and the Island

    This Enum represents the different was agents can communicate with each other and with the
    Island. The value of each member is the member's name in all lower-case characters.
    """

    SCANNED = "scanned"
    EXPLOITED = "exploited"
    CC = "cc"
