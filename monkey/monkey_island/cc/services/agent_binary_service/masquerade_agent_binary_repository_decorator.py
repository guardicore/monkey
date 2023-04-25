import io
from functools import lru_cache
from typing import BinaryIO

from .i_agent_binary_repository import IAgentBinaryRepository

NULL_BYTES_LENGTH = 16


class MasqueradeAgentBinaryRepositoryDecorator(IAgentBinaryRepository):
    """
    An IAgentBinaryRepsitory decorator that applies a masque to the
    agent binaries for other IAgentBinaryRepositories
    """

    def __init__(self, agent_binary_repository: IAgentBinaryRepository, masque: bytes):
        self._agent_binary_repository = agent_binary_repository
        self._masque = masque

    @lru_cache()
    def get_linux_binary(self) -> BinaryIO:
        agent_linux_binary = self._agent_binary_repository.get_linux_binary()
        return self._apply_masque(agent_linux_binary)

    @lru_cache()
    def get_windows_binary(self) -> BinaryIO:
        agent_windows_binary = self._agent_binary_repository.get_windows_binary()
        return self._apply_masque(agent_windows_binary)

    def _apply_masque(self, agent_binary: BinaryIO) -> BinaryIO:
        null_bytes = b"\x00" * NULL_BYTES_LENGTH
        agent_binary.seek(0, io.SEEK_END)
        agent_binary.write(null_bytes + self._masque)
        return agent_binary
