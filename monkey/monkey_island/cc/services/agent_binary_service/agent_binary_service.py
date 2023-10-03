from typing import BinaryIO, Optional

from monkeytypes import OperatingSystem

from . import IAgentBinaryService
from .i_agent_binary_repository import IAgentBinaryRepository
from .i_masquerade_repository import IMasqueradeRepository
from .masquerade_agent_binary_repository_decorator import MasqueradeAgentBinaryRepositoryDecorator


class AgentBinaryService(IAgentBinaryService):
    """
    A service for retrieving and manipulating agent binaries
    """

    def __init__(
        self,
        agent_binary_repository: IAgentBinaryRepository,
        masquerade_repository: IMasqueradeRepository,
    ):
        self._masquerade_repository = masquerade_repository
        self._agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
            agent_binary_repository, self._masquerade_repository
        )

    def get_agent_binary(self, operating_system: OperatingSystem) -> BinaryIO:
        return self._agent_binary_repository.get_agent_binary(operating_system)

    def get_masque(self, operating_system: OperatingSystem) -> Optional[bytes]:
        return self._masquerade_repository.get_masque(operating_system)

    def set_masque(self, operating_system: OperatingSystem, masque: Optional[bytes]):
        self._masquerade_repository.set_masque(operating_system, masque)
