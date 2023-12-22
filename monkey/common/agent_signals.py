from datetime import datetime
from typing import Optional

from monkeytypes.base_models import InfectionMonkeyBaseModel


class AgentSignals(InfectionMonkeyBaseModel):
    terminate: Optional[datetime]
