from __future__ import annotations

from datetime import datetime
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel


class Simulation(InfectionMonkeyBaseModel):
    terminate_signal_time: Optional[datetime] = None
