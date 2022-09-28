import io

from monkey_island.cc import repository
from monkey_island.cc.models import AgentID
from monkey_island.cc.repository import (
    IAgentLogRepository,
    IFileRepository,
    RetrievalError,
    UnknownRecordError,
)

AGENT_LOG_FILE_NAME_PREFIX = "agent_log_"


class FileAgentLogRepository(IAgentLogRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def upsert_agent_log(self, agent_id: AgentID, log_contents: str):
        self._file_repository.save_file(
            f"{AGENT_LOG_FILE_NAME_PREFIX}{agent_id}", io.BytesIO(log_contents.encode())
        )

    def get_agent_log(self, agent_id: AgentID) -> str:
        try:
            with self._file_repository.open_file(f"{AGENT_LOG_FILE_NAME_PREFIX}{agent_id}") as f:
                log_contents = f.read().decode()
                return log_contents
        except repository.FileNotFoundError as err:
            raise UnknownRecordError(err)
        except Exception as err:
            raise RetrievalError(f"Error retrieving the agent logs: {err}")

    def reset(self):
        self._file_repository.delete_files_by_pattern(f"{AGENT_LOG_FILE_NAME_PREFIX}*")
