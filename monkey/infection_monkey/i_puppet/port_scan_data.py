from typing import Optional

from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel
from common.types import NetworkPort, NetworkProtocol, NetworkService, PortStatus


class PortScanData(InfectionMonkeyBaseModel):
    port: NetworkPort
    status: PortStatus
    protocol: Optional[NetworkProtocol]
    banner: Optional[str] = Field(default=None)
    service: NetworkService = Field(default=NetworkService.UNKNOWN)
    service_deprecated: Optional[str] = Field(default=None)
