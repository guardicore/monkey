from __future__ import annotations

from datetime import datetime
from typing import Optional

from common.base_models import InfectionMonkeyBaseModel


class Simulation(InfectionMonkeyBaseModel):
    terminate_signal_time: Optional[datetime] = None
