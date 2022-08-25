from ipaddress import IPv4Interface
from typing import Optional, Sequence

from pydantic import Field, PositiveInt, validator

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.transforms import make_immutable_sequence
from common.types import HardwareID

MachineID = PositiveInt


class Machine(MutableInfectionMonkeyBaseModel):
    id: MachineID = Field(..., allow_mutation=False)
    hardware_id: Optional[HardwareID]
    network_interfaces: Sequence[IPv4Interface]
    operating_system: OperatingSystem
    operating_system_version: str
    hostname: str

    _make_immutable_sequence = validator("network_interfaces", pre=True, allow_reuse=True)(
        make_immutable_sequence
    )
