from typing import List, Optional

from monkeytypes import DiscoveredService, InfectionMonkeyBaseModel, OperatingSystem


class FingerprintData(InfectionMonkeyBaseModel):
    os_type: Optional[OperatingSystem]
    os_version: Optional[str]
    services: List[DiscoveredService]
