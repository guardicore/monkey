from enum import Enum


class Deployment(Enum):
    DEVELOP = "develop"
    WINDOWS = "windows"
    APPIMAGE = "appimage"
    DOCKER = "docker"
