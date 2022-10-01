from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from ipaddress import IPv4Address
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import ConstrainedInt, PositiveInt
from typing_extensions import TypeAlias

from common import OperatingSystem
from common.base_models import InfectionMonkeyBaseModel
from common.network.network_utils import address_to_ip_port

AgentID: TypeAlias = UUID
HardwareID: TypeAlias = PositiveInt
MachineID: TypeAlias = PositiveInt

JSONSerializable = Union[  # type: ignore[misc]
    Dict[str, "JSONSerializable"],  # type: ignore[misc]
    List["JSONSerializable"],  # type: ignore[misc]
    int,
    str,
    float,
    bool,
    None,
]


class NetworkPort(ConstrainedInt):
    """
    Define network port as constrainer integer.

    To define a default value with this type:
        port: NetworkPort = typing.cast(NetworkPort, 1000)
    """

    ge = 0
    le = 65535


@dataclass
class PingScanData:
    response_received: bool
    os: Optional[OperatingSystem]


class PortStatus(Enum):
    """
    An Enum representing the status of the port.

    This Enum represents the status of a network pork. The value of each
    member is the member's name in all lower-case characters.
    """

    OPEN = "open"
    CLOSED = "closed"


class SocketAddress(InfectionMonkeyBaseModel):
    ip: IPv4Address
    port: NetworkPort

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

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f"{self.ip}:{self.port}"
