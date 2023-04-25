from typing import BinaryIO, Dict, Optional

from common import OperatingSystem

from . import IAgentBinaryService
from .i_agent_binary_repository import IAgentBinaryRepository


class AgentBinaryService(IAgentBinaryService):
    """
    A service for retrieving and manipulating agent binaries
    """

    def __init__(self, agent_binary_repository: IAgentBinaryRepository):
        self._agent_binary_repository = agent_binary_repository

        self._os_masque: Dict[OperatingSystem, Optional[bytes]] = {
            OperatingSystem.LINUX: None,
            OperatingSystem.WINDOWS: None,
        }

    def get_linux_binary(self) -> BinaryIO:
        return self._agent_binary_repository.get_linux_binary()

    def get_windows_binary(self) -> BinaryIO:
        return self._agent_binary_repository.get_windows_binary()

    def get_masque(self, operating_system: OperatingSystem) -> Optional[bytes]:
        return self._os_masque.get(operating_system, None)

    def set_masque(self, operating_system: OperatingSystem, masque: Optional[bytes]):
        self._os_masque[operating_system] = masque
