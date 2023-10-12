import pprint
from collections import UserDict
from ipaddress import IPv4Address
from typing import Optional, Set

from monkeytypes import MutableInfectionMonkeyBaseModel, NetworkPort, OperatingSystem, PortStatus
from pydantic import ConfigDict, Field, field_serializer, validate_call

from . import PortScanData


class PortScanDataDict(UserDict[NetworkPort, PortScanData]):
    @validate_call
    def __setitem__(self, key: NetworkPort, value: PortScanData):
        super().__setitem__(key, value)

    @property
    def open(self) -> Set[NetworkPort]:
        return self._filter_ports_by_status(PortStatus.OPEN)

    @property
    def closed(self) -> Set[NetworkPort]:
        return self._filter_ports_by_status(PortStatus.CLOSED)

    def _filter_ports_by_status(self, status: PortStatus) -> Set[NetworkPort]:
        return {
            port for port, port_scan_data in self.data.items() if port_scan_data.status == status
        }


class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tcp_ports: PortScanDataDict = Field(default_factory=PortScanDataDict)
    udp_ports: PortScanDataDict = Field(default_factory=PortScanDataDict)

    @field_serializer("tcp_ports", "udp_ports", when_used="json")
    def dump_ports(self, v):
        return dict(v)


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    icmp: bool = Field(default=False)
    ports_status: TargetHostPorts = Field(default=TargetHostPorts())

    def __hash__(self):
        return hash(self.ip)

    def __str__(self):
        return pprint.pformat(self.model_dump(mode="json"))
