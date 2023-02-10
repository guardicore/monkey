from datetime import datetime

from common.base_models import InfectionMonkeyBaseModel


class TerminateAllAgents(InfectionMonkeyBaseModel):
    timestamp: datetime
