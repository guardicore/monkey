from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel
from pydantic import Field

from common.types import NetworkPort, NetworkProtocol, NetworkService, PortStatus


class PortScanData(InfectionMonkeyBaseModel):
    port: NetworkPort
    status: PortStatus
    protocol: NetworkProtocol = Field(default=NetworkProtocol.UNKNOWN)
    banner: Optional[str] = Field(default=None)
    service: NetworkService = Field(default=NetworkService.UNKNOWN)
