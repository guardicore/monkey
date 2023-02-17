from typing import List, Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import InfectionMonkeyBaseModel
from common.types import NetworkService


class FingerprintData(InfectionMonkeyBaseModel):
    os_type: Optional[OperatingSystem]
    os_version: Optional[str]
    services: List[NetworkService] = Field(default=[])
