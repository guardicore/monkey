from enum import Enum


class Deployment(Enum):
    """
    An Enum representing the different ways the Island can be deployed

    The Infection Monkey Island can be deployed on a variety of different platforms via different
    packaging mechanisms. This Enum represents the different ways that the Island can be deployed.
    The value of each member is the member's name in all lower-case characters.
    """

    DEVELOP = "develop"
    WINDOWS = "windows"
    APPIMAGE = "appimage"
    DOCKER = "docker"
