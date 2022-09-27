from __future__ import annotations

from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Optional
from uuid import UUID

from pydantic import PositiveInt, conint
from typing_extensions import TypeAlias

from common import OperatingSystem
from common.base_models import InfectionMonkeyBaseModel
from common.network.network_utils import address_to_ip_port

AgentID: TypeAlias = UUID
HardwareID: TypeAlias = PositiveInt
MachineID: TypeAlias = PositiveInt


@dataclass
class PingScanData:
    response_received: bool
    os: Optional[OperatingSystem]


class SocketAddress(InfectionMonkeyBaseModel):
    ip: IPv4Address
    port: conint(ge=1, le=65535)  # type: ignore[valid-type]

    @classmethod
    def from_string(cls, address_str: str) -> SocketAddress:
        """
        Parse a SocketAddress object from a string

        :param address_str: A string of ip:port
        :raises ValueError: If the string is not a valid ip:port
        :return: SocketAddress with the IP and port
        """
        ip, port = address_to_ip_port(address_str)
        if port is None:
            raise ValueError("SocketAddress requires a port")
        return SocketAddress(ip=IPv4Address(ip), port=int(port))

    def __str__(self):
        return f"{self.ip}:{self.port}"
