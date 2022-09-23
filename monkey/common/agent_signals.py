from datetime import datetime
from typing import Optional

from .base_models import InfectionMonkeyBaseModel


class AgentSignals(InfectionMonkeyBaseModel):
    terminate: Optional[datetime]
