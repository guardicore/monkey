from datetime import datetime, timezone
from typing import Dict

from common import AgentHeartbeat
from common.common_consts import HEARTBEAT_INTERVAL
from common.types import AgentID
from monkey_island.cc.repositories import IAgentRepository

DEFAULT_HEARTBEAT_TIMEOUT = 3 * HEARTBEAT_INTERVAL


class AgentHeartbeatHandler:
    """
    Tracks Agents' latest heartbeats and handles related functionality
    """

    def __init__(
        self, agent_repository: IAgentRepository, heartbeat_timeout=DEFAULT_HEARTBEAT_TIMEOUT
    ):
        self._agent_repository = agent_repository
        self._heartbeat_timeout = heartbeat_timeout
        self._latest_heartbeats: Dict[AgentID, datetime] = {}

    def handle_agent_heartbeat(self, agent_id: AgentID, heartbeat: AgentHeartbeat):
        self._latest_heartbeats[agent_id] = heartbeat.timestamp

    def set_unresponsive_agents_stop_time(self):
        agents = self._agent_repository.get_running_agents()
        current_time = datetime.now(tz=timezone.utc)

        for agent in agents:
            latest_heartbeat = self._latest_heartbeats.get(agent.id, agent.start_time)

            if (current_time - latest_heartbeat).total_seconds() >= self._heartbeat_timeout:
                agent.stop_time = latest_heartbeat
                self._agent_repository.upsert_agent(agent)
