from typing import BinaryIO

from monkeytypes import OperatingSystem

from monkey_island.cc.repositories import IFileRepository, RetrievalError

from .i_agent_binary_repository import IAgentBinaryRepository

LINUX_AGENT_FILE_NAME = "monkey-linux-64"
WINDOWS_AGENT_FILE_NAME = "monkey-windows-64.exe"

AGENT_FILE_NAMES = {
    OperatingSystem.LINUX: LINUX_AGENT_FILE_NAME,
    OperatingSystem.WINDOWS: WINDOWS_AGENT_FILE_NAME,
}


class AgentBinaryRepository(IAgentBinaryRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def get_agent_binary(self, operating_system: OperatingSystem) -> BinaryIO:
        return self._get_binary(AGENT_FILE_NAMES[operating_system])

    def _get_binary(self, filename: str) -> BinaryIO:
        try:
            agent_binary = self._file_repository.open_file(filename)
            return agent_binary
        except Exception as err:
            raise RetrievalError(
                f"An error occurred while retrieving the {filename}"
                f" agent binary from {self._file_repository}: {err}"
            )
