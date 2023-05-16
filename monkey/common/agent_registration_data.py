from datetime import datetime
from ipaddress import IPv4Interface
from typing import Optional, Sequence
from uuid import UUID

from pydantic import Field, validator

from .base_models import InfectionMonkeyBaseModel
from .transforms import make_immutable_sequence
from .types import HardwareID, SocketAddress


class AgentRegistrationData(InfectionMonkeyBaseModel):
    id: UUID
    machine_hardware_id: HardwareID
    start_time: datetime
    parent_id: Optional[UUID]
    cc_server: SocketAddress
    network_interfaces: Sequence[IPv4Interface]
    sha256: str = Field(regex=r"^[0-9a-fA-F]{64}$")

    _make_immutable_sequence = validator("network_interfaces", pre=True, allow_reuse=True)(
        make_immutable_sequence
    )
