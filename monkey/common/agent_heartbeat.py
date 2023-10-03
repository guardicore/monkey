from datetime import datetime

from monkeytypes.base_models import InfectionMonkeyBaseModel


class AgentHeartbeat(InfectionMonkeyBaseModel):
    timestamp: datetime
