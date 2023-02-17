from typing import List, Optional

from common import OperatingSystem
from common.base_models import InfectionMonkeyBaseModel
from common.types import NetworkPort, NetworkProtocol, NetworkService


class DiscoveredService(InfectionMonkeyBaseModel):
    protocol: NetworkProtocol
    port: NetworkPort
    services: NetworkService


class FingerprintData(InfectionMonkeyBaseModel):
    os_type: Optional[OperatingSystem]
    os_version: Optional[str]
    services: List[DiscoveredService]
