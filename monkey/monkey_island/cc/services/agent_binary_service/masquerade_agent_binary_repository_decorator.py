import io
from functools import lru_cache
from typing import BinaryIO, Mapping, Optional

from common import OperatingSystem
from common.utils.file_utils import make_fileobj_copy

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
        masques: Mapping[OperatingSystem, Optional[bytes]],
        null_bytes_length: int = DEFAULT_NULL_BYTES_LENGTH,
    ):
        self._agent_binary_repository = agent_binary_repository
        self._masques = masques
        self._null_bytes = b"\x00" * null_bytes_length

    def get_agent_binary(self, operating_system: OperatingSystem) -> BinaryIO:
        original_file = self._get_agent_binary(operating_system)

        return make_fileobj_copy(original_file)

    @lru_cache()
    def _get_agent_binary(self, operating_system: OperatingSystem) -> BinaryIO:
        agent_binary = self._agent_binary_repository.get_agent_binary(operating_system)
        return self._apply_masque(operating_system, agent_binary)

    def _apply_masque(self, operating_system: OperatingSystem, agent_binary: BinaryIO) -> BinaryIO:
        masque = self._masques.get(operating_system, None)

        if masque is None:
            return agent_binary

        # Note: These null bytes separate the Agent binary from the masque. The goal is to prevent
        # the masque from being interpreted by the OS as code that should be run.
        agent_binary.seek(0, io.SEEK_END)
        agent_binary.write(self._null_bytes + masque)
        agent_binary.seek(0)

        return agent_binary
