import io
import re

from monkey_island.cc.models import AgentID
from monkey_island.cc.repositories import IFileRepository, RepositoryError, RetrievalError
from . import IAgentLogRepository

AGENT_LOG_FILE_NAME_REGEX = re.compile(r"^agent-[\w-]+.log$")


class FileAgentLogRepository(IAgentLogRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def upsert_agent_log(self, agent_id: AgentID, log_contents: str):
        log_file_name = FileAgentLogRepository._get_agent_log_file_name(agent_id)
        self._file_repository.save_file(log_file_name, io.BytesIO(log_contents.encode()))

    def get_agent_log(self, agent_id: AgentID) -> str:
        log_file_name = FileAgentLogRepository._get_agent_log_file_name(agent_id)

        try:
            with self._file_repository.open_file(log_file_name) as f:
                log_contents = f.read().decode()
                return log_contents
        except RepositoryError as err:
            raise err
        except Exception as err:
            raise RetrievalError(f"Error retrieving the agent logs: {err}")

    def reset(self):
        self._file_repository.delete_files_by_regex(AGENT_LOG_FILE_NAME_REGEX)

    @staticmethod
    def _get_agent_log_file_name(agent_id: AgentID) -> str:
        return f"agent-{agent_id}.log"
