from typing import Optional

from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel
from common.types import NetworkPort, NetworkService, PortStatus


class PortScanData(InfectionMonkeyBaseModel):
    port: NetworkPort
    status: PortStatus
    banner: Optional[str] = Field(default=None)
    service: NetworkService = Field(default=NetworkService.UNKNOWN)
    service_deprecated: Optional[str] = Field(default=None)
