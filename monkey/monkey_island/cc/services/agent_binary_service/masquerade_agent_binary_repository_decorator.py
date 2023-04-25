import io
from functools import lru_cache
from typing import BinaryIO

from .i_agent_binary_repository import IAgentBinaryRepository

DEFAULT_NULL_BYTES_LENGTH = 16


class MasqueradeAgentBinaryRepositoryDecorator(IAgentBinaryRepository):
    """
    An IAgentBinaryRepsitory decorator that applies a masque Agent binaries


    This decorator applies a masque by appending a fixed set of bytes to Agent binaries. The masque
    is preceeded by a configurable number of null bytes to prevent the masque from being interpreted
    as part of the binary.
    """

    def __init__(
        self,
        agent_binary_repository: IAgentBinaryRepository,
        masque: bytes,
        null_bytes_length: int = DEFAULT_NULL_BYTES_LENGTH,
    ):
        self._agent_binary_repository = agent_binary_repository
        self._masque = masque
        self._null_bytes_length = null_bytes_length

    @lru_cache()
    def get_linux_binary(self) -> BinaryIO:
        agent_linux_binary = self._agent_binary_repository.get_linux_binary()
        return self._apply_masque(agent_linux_binary)

    @lru_cache()
    def get_windows_binary(self) -> BinaryIO:
        agent_windows_binary = self._agent_binary_repository.get_windows_binary()
        return self._apply_masque(agent_windows_binary)

    def _apply_masque(self, agent_binary: BinaryIO) -> BinaryIO:
        # Note: These null bytes separate the Agent binary from the masque. The goal is to prevent
        # the masque from being interpreted by the OS as code that should be run.
        null_bytes = b"\x00" * self._null_bytes_length
        agent_binary.seek(0, io.SEEK_END)
        agent_binary.write(null_bytes + self._masque)
        return agent_binary
