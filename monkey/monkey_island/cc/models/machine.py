import json
from ipaddress import IPv4Interface
from typing import Any, Dict, Mapping, Optional, Tuple, TypeAlias

from monkeytypes import (
    HardwareID,
    MutableInfectionMonkeyBaseModel,
    MutableInfectionMonkeyModelConfig,
    NetworkService,
    OperatingSystem,
    SocketAddress,
)
from pydantic import Field, validator

from . import MachineID

NetworkServices: TypeAlias = Dict[SocketAddress, NetworkService]


def _serialize_network_services(machine_dict: Dict, *, default):
    machine_dict["network_services"] = {
        str(addr): val for addr, val in machine_dict["network_services"].items()
    }
    return json.dumps(machine_dict, default=default)


class Machine(MutableInfectionMonkeyBaseModel):
    """Represents machines, VMs, or other network nodes discovered by Infection Monkey"""

    class Config(MutableInfectionMonkeyModelConfig):
        json_dumps = _serialize_network_services

    @validator("network_services", pre=True)
    def _socketaddress_from_string(cls, v: Any) -> Any:
        if not isinstance(v, Mapping):
            # Let pydantic's type validation handle this
            return v

        new_network_services = {}
        for addr, service in v.items():
            if isinstance(addr, SocketAddress):
                new_network_services[addr] = service
            else:
                new_network_services[SocketAddress.from_string(addr)] = service

        return new_network_services

    id: MachineID = Field(..., allow_mutation=False)
    """Uniquely identifies the machine within the island"""

    hardware_id: Optional[HardwareID] = Field(default=None)
    """An identifier generated by the agent that uniquely identifies a machine"""

    island: bool = Field(default=False, allow_mutation=False)
    """Whether or not the machine is an island (C&C server)"""

    network_interfaces: Tuple[IPv4Interface, ...] = tuple()
    """The machine's networking interfaces"""

    operating_system: Optional[OperatingSystem] = Field(default=None)
    """The operating system the machine is running"""

    operating_system_version: str = ""
    """The specific version of the operating system the machine is running"""

    hostname: str = ""
    """The hostname of the machine"""

    network_services: NetworkServices = Field(default_factory=dict)
    """All network services found running on the machine"""

    def __hash__(self):
        return self.id
