from datetime import datetime
from ipaddress import IPv4Interface
from typing import Optional
from uuid import UUID

from monkeytypes import InfectionMonkeyBaseModel, SocketAddress
from pydantic import Field

from .types import HardwareID


class AgentRegistrationData(InfectionMonkeyBaseModel):
    id: UUID
    machine_hardware_id: HardwareID
    start_time: datetime
    parent_id: Optional[UUID]
    cc_server: SocketAddress
    network_interfaces: tuple[IPv4Interface, ...]
    sha256: str = Field(pattern=r"^[0-9a-fA-F]{64}$")
