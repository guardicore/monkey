from typing import List, Optional

from monkeytypes import InfectionMonkeyBaseModel, OperatingSystem

from common.types import DiscoveredService


class FingerprintData(InfectionMonkeyBaseModel):
    os_type: Optional[OperatingSystem]
    os_version: Optional[str]
    services: List[DiscoveredService]
