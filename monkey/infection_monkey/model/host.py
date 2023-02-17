from ipaddress import IPv4Address
from typing import Any, Dict, Optional, Union

from pydantic import Field
from typing_extensions import Literal  # import from `typing` once we switch to Python 3.8

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel
from common.types import NetworkPort, NetworkProtocol
from infection_monkey.i_puppet import PortScanData


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    services: Dict[str, Any] = Field(default={})  # deprecated
    icmp: bool = Field(default=False)
    port_status: Dict[
        Union[Literal[NetworkProtocol.TCP], Literal[NetworkProtocol.UDP]],
        Dict[NetworkPort, PortScanData],
    ] = Field(default={})

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
