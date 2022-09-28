import io
import re

from monkey_island.cc.models import AgentID
from monkey_island.cc.repository import (
    IAgentLogRepository,
    IFileRepository,
    RepositoryError,
    RetrievalError,
)

AGENT_LOG_FILE_NAME_PATTERN = "agent-*.log"
AGENT_LOG_FILE_NAME_REGEX = re.compile(r"^agent-[\w-]+.log$")


class FileAgentLogRepository(IAgentLogRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def upsert_agent_log(self, agent_id: AgentID, log_contents: str):
        self._file_repository.save_file(
            self._get_agent_log_file_name(agent_id), io.BytesIO(log_contents.encode())
        )

    def get_agent_log(self, agent_id: AgentID) -> str:
        try:
            with self._file_repository.open_file(self._get_agent_log_file_name(agent_id)) as f:
                log_contents = f.read().decode()
                return log_contents
        except RepositoryError as err:
            raise err
        except Exception as err:
            raise RetrievalError(f"Error retrieving the agent logs: {err}")

    def reset(self):
        self._file_repository.delete_files_by_regex(AGENT_LOG_FILE_NAME_REGEX)

    def _get_agent_log_file_name(self, agent_id: AgentID) -> str:
        return AGENT_LOG_FILE_NAME_PATTERN.replace("*", str(agent_id))
