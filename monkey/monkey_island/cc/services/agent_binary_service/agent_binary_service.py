from typing import BinaryIO

from . import IAgentBinaryService
from .i_agent_binary_repository import IAgentBinaryRepository


class AgentBinaryService(IAgentBinaryService):
    """
    A service for retrieving and manipulating agent binaries
    """

    def __init__(self, agent_binary_repository: IAgentBinaryRepository):
        self._agent_binary_repository = agent_binary_repository

    def get_linux_binary(self) -> BinaryIO:
        return self._agent_binary_repository.get_linux_binary()

    def get_windows_binary(self) -> BinaryIO:
        return self._agent_binary_repository.get_windows_binary()
