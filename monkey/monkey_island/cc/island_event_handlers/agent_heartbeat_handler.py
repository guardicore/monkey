from datetime import datetime, timezone
from typing import Dict

from common import AgentHeartbeat
from common.common_consts import HEARTBEAT_INTERVAL
from common.types import AgentID
from monkey_island.cc.repositories import IAgentRepository


class AgentHeartbeatHandler:
    """
    Updates Agents with their heartbeat
    """

    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository
        self._last_agent_heartbeats: Dict[AgentID, datetime] = {}

    def update_agent_last_heartbeat(self, agent_id: AgentID, heartbeat: AgentHeartbeat):
        self._last_agent_heartbeats[agent_id] = heartbeat.timestamp

    def update_agents_stop_time_from_heartbeat(self):
        agents = self._agent_repository.get_running_agents()

        for agent in agents:
            last_agent_heartbeat = self._last_agent_heartbeats.get(agent.id)

            if last_agent_heartbeat is None:
                if (datetime.now(tz=timezone.utc) - agent.start_time).total_seconds() >= (
                    3 * HEARTBEAT_INTERVAL
                ):
                    agent.stop_time = agent.start_time
                    self._agent_repository.upsert_agent(agent)

            else:
                if (datetime.now(tz=timezone.utc) - last_agent_heartbeat).total_seconds() >= (
                    3 * HEARTBEAT_INTERVAL
                ):
                    agent.stop_time = last_agent_heartbeat
                    self._agent_repository.upsert_agent(agent)
