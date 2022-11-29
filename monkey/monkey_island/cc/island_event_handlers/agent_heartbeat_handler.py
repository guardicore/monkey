from datetime import datetime
from typing import Optional

from common.types import AgentID
from monkey_island.cc.repositories import IAgentRepository


class AgentHeartbeatHandler:
    """
    Updates Agents with their heartbeat
    """

    def __init__(
        self,
        agent_repository: IAgentRepository,
    ):
        self._agent_repository = agent_repository

    def __call__(self, agent_id: AgentID, timestamp: Optional[datetime]):
        agent = self._agent_repository.get_agent_by_id(agent_id)
        agent.last_heartbeat_time = timestamp

        self._agent_repository.upsert_agent(agent)
