from ipaddress import IPv4Address
from typing import Any, Dict, Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.types import NetworkPort

from . import PortScanData


# TODO: do we really need this? Can't we just have
# `TargetHost.ports_status` be `Dict[NetworkPort, PortScanData]`?
# `PortScanData` already has protocol information so having `tcp_ports`
# and `udp_ports` is redundant.
class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    tcp_ports: Dict[NetworkPort, PortScanData] = Field(default={})
    udp_ports: Dict[NetworkPort, PortScanData] = Field(default={})


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    services: Dict[str, Any] = Field(default={})  # deprecated
    icmp: bool = Field(default=False)
    ports_status: TargetHostPorts = Field(default=TargetHostPorts())

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
