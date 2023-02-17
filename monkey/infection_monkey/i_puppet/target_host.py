from ipaddress import IPv4Address
from typing import Any, Dict, List, Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.types import NetworkPort

from . import PortScanData


class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    tcp_ports: List[Dict[NetworkPort, PortScanData]] = Field(default=[])
    udp_ports: List[Dict[NetworkPort, PortScanData]] = Field(default=[])


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    services: Dict[str, Any] = Field(default={})  # deprecated
    icmp: bool = Field(default=False)
    ports_status: Optional[TargetHostPorts]

    def __hash__(self):
        return hash(self.ip)

    def __str__(self):
        victim = "Target Host %s: " % self.ip
        if self.operating_system is not None:
            victim += "OS - [ %s ]" % self.operating_system.value
        victim += "Services - ["
        for k, v in list(self.services.items()):
            victim += "%s-%s " % (k, v)
        victim += "] ICMP: %s " % (self.icmp)
        return victim
