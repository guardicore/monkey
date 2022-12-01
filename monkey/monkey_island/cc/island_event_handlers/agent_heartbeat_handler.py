import logging
from datetime import datetime, timezone
from typing import Dict

from common import AgentHeartbeat
from common.common_consts import HEARTBEAT_INTERVAL
from common.types import AgentID
from monkey_island.cc.repositories import IAgentRepository

logger = logging.getLogger(__name__)


class AgentHeartbeatHandler:
    """
    Tracks Agents' latest heartbeats and handles related functionality
    """

    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository
        self._latest_heartbeats: Dict[AgentID, datetime] = {}

    def update_latest_heartbeat_of_agent(self, agent_id: AgentID, heartbeat: AgentHeartbeat):
        self._latest_heartbeats[agent_id] = heartbeat.timestamp
        self._reset_stop_time_if_agent_previously_marked_dead(agent_id)

    def _reset_stop_time_if_agent_previously_marked_dead(self, agent_id: AgentID):
        logger.info(
            f"Received a heartbeat from agent {agent_id} previously marked as stopped. "
            "Resetting its stop time."
        )
        agent = self._agent_repository.get_agent_by_id(agent_id)
        agent.stop_time = None
        self._agent_repository.upsert_agent(agent)

    def check_status_of_agents_from_latest_heartbeats(self):
        agents = self._agent_repository.get_running_agents()

        for agent in agents:
            latest_heartbeat = self._latest_heartbeats.get(agent.id)

            if latest_heartbeat is None:
                if (datetime.now(tz=timezone.utc) - agent.start_time).total_seconds() >= (
                    3 * HEARTBEAT_INTERVAL
                ):
                    agent.stop_time = agent.start_time
                    self._agent_repository.upsert_agent(agent)

            else:
                if (datetime.now(tz=timezone.utc) - latest_heartbeat).total_seconds() >= (
                    3 * HEARTBEAT_INTERVAL
                ):
                    agent.stop_time = latest_heartbeat
                    self._agent_repository.upsert_agent(agent)
