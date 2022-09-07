from __future__ import annotations

from enum import Enum

from common.base_models import InfectionMonkeyBaseModel


class IslandMode(Enum):
    UNSET = "unset"
    RANSOMWARE = "ransomware"
    ADVANCED = "advanced"


class Simulation(InfectionMonkeyBaseModel):
    mode: IslandMode = IslandMode.UNSET
