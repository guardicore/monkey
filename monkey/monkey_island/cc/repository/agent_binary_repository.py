from typing import BinaryIO

from . import AgentRetrivalError, FileRetrivalError, IAgentBinaryRepository, IFileRepository

LINUX_AGENT_FILE_NAME = "monkey-linux-64"
WINDOWS_AGENT_FILE_NAME = "monkey-windows-64.exe"


class AgentBinaryRepository(IAgentBinaryRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def get_linux_binary(self) -> BinaryIO:
        try:
            agent_binary = self._file_repository.open_file(LINUX_AGENT_FILE_NAME)
            return agent_binary
        except FileRetrivalError as err:
            raise AgentRetrivalError(
                f"An error occurred while retrieving the Linux agent binary: {err}"
            )

    def get_windows_binary(self) -> BinaryIO:
        try:
            agent_binary = self._file_repository.open_file(WINDOWS_AGENT_FILE_NAME)
            return agent_binary
        except FileRetrivalError as err:
            raise AgentRetrivalError(
                f"An error occurred while retrieving the Windows agent binary: {err}"
            )
