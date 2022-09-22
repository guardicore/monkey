from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from common.base_models import InfectionMonkeyBaseModel


class IslandMode(Enum):
    UNSET = "unset"
    RANSOMWARE = "ransomware"
    ADVANCED = "advanced"


class Simulation(InfectionMonkeyBaseModel):
    mode: IslandMode = IslandMode.UNSET
    terminate_signal_time: Optional[datetime] = None
