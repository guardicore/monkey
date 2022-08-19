from ipaddress import IPv4Interface
from typing import Optional, Sequence

from pydantic import Field, PositiveInt, validator

from common import OperatingSystem

from .base_models import MutableBaseModel
from .transforms import make_immutable_sequence

MachineID = PositiveInt


class Machine(MutableBaseModel):
    id: MachineID = Field(..., allow_mutation=False)
    hardware_id: Optional[PositiveInt]
    network_interfaces: Sequence[IPv4Interface]
    operating_system: OperatingSystem
    operating_system_version: str
    hostname: str

    _make_immutable_sequence = validator("network_interfaces", pre=True, allow_reuse=True)(
        make_immutable_sequence
    )
