from datetime import datetime

from common.base_models import InfectionMonkeyBaseModel


class AgentHeartbeat(InfectionMonkeyBaseModel):
    timestamp: datetime
