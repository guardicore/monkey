from typing import Dict, Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import InfectionMonkeyBaseModel


class FingerprintData(InfectionMonkeyBaseModel):
    os_type: Optional[OperatingSystem]
    os_version: Optional[str]
    services: Dict[str, Dict[str, str]] = Field(default={})
