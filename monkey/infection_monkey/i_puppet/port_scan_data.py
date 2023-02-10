from typing import Optional

from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel
from common.types import NetworkPort, PortStatus


class PortScanData(InfectionMonkeyBaseModel):
    port: NetworkPort
    status: PortStatus
    banner: Optional[str] = Field(default=None)
    service: Optional[str] = Field(default=None)
