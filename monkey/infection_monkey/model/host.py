from ipaddress import IPv4Address
from typing import Any, Dict, Optional

from pydantic import Field

from common import OperatingSystem
from common.base_models import MutableInfectionMonkeyBaseModel


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    services: Dict[str, Any] = Field(default={})  # deprecated
    icmp: bool = Field(default=False)

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
