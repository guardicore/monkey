import pprint
from ipaddress import IPv4Address
from typing import Dict, Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.types import NetworkPort

from . import PortScanData


class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    tcp_ports: Dict[NetworkPort, PortScanData] = Field(default={})
    udp_ports: Dict[NetworkPort, PortScanData] = Field(default={})


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    icmp: bool = Field(default=False)
    ports_status: TargetHostPorts = Field(default=TargetHostPorts())

    def __hash__(self):
        return hash(self.ip)

    def __str__(self):
        return pprint.pformat(self.dict(simplify=True))
