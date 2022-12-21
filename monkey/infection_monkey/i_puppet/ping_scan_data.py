from typing import Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import InfectionMonkeyBaseModel


class PingScanData(InfectionMonkeyBaseModel):
    response_received: bool
    os: Optional[OperatingSystem] = Field(default=None)
