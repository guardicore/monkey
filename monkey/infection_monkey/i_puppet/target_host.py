import pprint
from ipaddress import IPv4Address
from typing import Callable, Dict, Optional, Sequence

from pydantic import Field

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.types import NetworkPort

from . import PortScanData

FilterPortFunc = Callable[[PortScanData], bool]


class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    tcp_ports: Dict[NetworkPort, PortScanData] = Field(default={})
    udp_ports: Dict[NetworkPort, PortScanData] = Field(default={})


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    icmp: bool = Field(default=False)
    ports_status: TargetHostPorts = Field(default=TargetHostPorts())

    def filter_selected_tcp_ports(
        self, ports: Sequence[NetworkPort], filter: FilterPortFunc
    ) -> Sequence[PortScanData]:
        return [
            p
            for p in ports
            if p in self.ports_status.tcp_ports and filter(self.ports_status.tcp_ports[p])
        ]

    def __hash__(self):
        return hash(self.ip)

    def __str__(self):
        return pprint.pformat(self.dict(simplify=True))
