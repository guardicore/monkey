from monkeytypes import AgentID

from monkey_island.cc.repositories import UnknownRecordError
from monkey_island.cc.services.log_service.i_agent_log_repository import IAgentLogRepository


class InMemoryAgentLogRepository(IAgentLogRepository):
    def __init__(self):
        self._agent_logs = {}

    def upsert_agent_log(self, agent_id: AgentID, log_contents: str):
        if agent_id not in self._agent_logs.keys():
            self._agent_logs[agent_id] = log_contents

    def get_agent_log(self, agent_id: AgentID) -> str:
        if agent_id not in self._agent_logs:
            raise UnknownRecordError(f"Unknown agent {agent_id}")

        return self._agent_logs[agent_id]

    def reset(self):
        self._agent_logs = {}
