from datetime import datetime

from monkeytypes import InfectionMonkeyBaseModel


class TerminateAllAgents(InfectionMonkeyBaseModel):
    timestamp: datetime
