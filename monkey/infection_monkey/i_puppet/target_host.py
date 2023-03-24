import pprint
from collections import UserDict
from ipaddress import IPv4Address
from typing import Dict, Optional, Set

from pydantic import Field, validate_arguments

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.types import NetworkPort, PortStatus

from . import PortScanData


class PortScanDataDict(UserDict[NetworkPort, PortScanData]):
    @validate_arguments
    def __setitem__(self, key: NetworkPort, value: PortScanData):
        super().__setitem__(key, value)


class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    tcp_ports: Dict[NetworkPort, PortScanData] = Field(default={})
    udp_ports: Dict[NetworkPort, PortScanData] = Field(default={})

    @property
    def closed_tcp_ports(self) -> Set[NetworkPort]:
        return {
            port
            for port, port_scan_data in self.tcp_ports.items()
            if port_scan_data.status == PortStatus.CLOSED
        }


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    icmp: bool = Field(default=False)
    ports_status: TargetHostPorts = Field(default=TargetHostPorts())

    def __hash__(self):
        return hash(self.ip)

    def __str__(self):
        return pprint.pformat(self.dict(simplify=True))
