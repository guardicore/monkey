from typing import Optional

from monkeytypes import OperatingSystem
from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel


class PingScanData(InfectionMonkeyBaseModel):
    response_received: bool
    os: Optional[OperatingSystem] = Field(default=None)
