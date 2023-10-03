from typing import Dict, Optional

from monkeytypes import OperatingSystem

from monkey_island.cc.services.agent_binary_service.i_masquerade_repository import (
    IMasqueradeRepository,
)


class InMemoryMasqueradeRepository(IMasqueradeRepository):
    def __init__(self) -> None:
        self._os_masque: Dict[OperatingSystem, Optional[bytes]] = {
            OperatingSystem.LINUX: None,
            OperatingSystem.WINDOWS: None,
        }

    def get_masque(self, operating_system: OperatingSystem) -> Optional[bytes]:
        return self._os_masque.get(operating_system, None)

    def set_masque(self, operating_system: OperatingSystem, masque: Optional[bytes]):
        self._os_masque[operating_system] = masque

    def reset(self):
        self.set_masque(OperatingSystem.LINUX, None)
        self.set_masque(OperatingSystem.WINDOWS, None)
