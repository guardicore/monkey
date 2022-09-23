from ipaddress import IPv4Address
from uuid import UUID

from pydantic import PositiveInt, conint
from typing_extensions import TypeAlias

from common.base_models import InfectionMonkeyBaseModel

AgentID: TypeAlias = UUID
HardwareID: TypeAlias = PositiveInt
MachineID: TypeAlias = PositiveInt


class SocketAddress(InfectionMonkeyBaseModel):
    ip: IPv4Address
    port: conint(ge=1, le=65535)  # type: ignore[valid-type]

    def __str__(self):
        return f"{self.ip}:{self.port}"
