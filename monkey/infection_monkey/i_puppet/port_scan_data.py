from typing import Optional

from monkeytypes import (
    InfectionMonkeyBaseModel,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    PortStatus,
)
from pydantic import Field


class PortScanData(InfectionMonkeyBaseModel):
    port: NetworkPort
    status: PortStatus
    protocol: NetworkProtocol = Field(default=NetworkProtocol.UNKNOWN)
    banner: Optional[str] = Field(default=None)
    service: NetworkService = Field(default=NetworkService.UNKNOWN)
