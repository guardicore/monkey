from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel, OperatingSystem
from pydantic import Field


class PingScanData(InfectionMonkeyBaseModel):
    response_received: bool
    os: Optional[OperatingSystem] = Field(default=None)
