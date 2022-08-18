from ipaddress import IPv4Interface
from typing import Optional, Sequence

from pydantic import Field, PositiveInt

from common import OperatingSystems

from .base_models import MutableBaseModel


class Machine(MutableBaseModel):
    id: PositiveInt = Field(..., allow_mutation=False)
    node_id: Optional[PositiveInt]
    network_interfaces: Sequence[IPv4Interface]
    operating_system: OperatingSystems
    operating_system_version: str
    hostname: str
