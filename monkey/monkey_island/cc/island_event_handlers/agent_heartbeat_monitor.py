import logging
from datetime import datetime, timezone
from typing import Dict, Sequence

from monkeytypes import AgentID

from common import AgentHeartbeat
from common.common_consts import HEARTBEAT_INTERVAL
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import Agent
from monkey_island.cc.repositories import IAgentRepository

DEFAULT_HEARTBEAT_TIMEOUT = 3 * HEARTBEAT_INTERVAL

logger = logging.getLogger(__name__)


class AgentHeartbeatMonitor:
    """
    Tracks Agents' latest heartbeats and handles related functionality
    """

    def __init__(
        self,
        agent_repository: IAgentRepository,
        island_event_queue: IIslandEventQueue,
        heartbeat_timeout=DEFAULT_HEARTBEAT_TIMEOUT,
    ):
        self._agent_repository = agent_repository
        self._island_event_queue = island_event_queue
        self._heartbeat_timeout = heartbeat_timeout
        self._latest_heartbeats: Dict[AgentID, datetime] = {}

    def handle_agent_heartbeat(self, agent_id: AgentID, heartbeat: AgentHeartbeat):
        self._latest_heartbeats[agent_id] = heartbeat.timestamp

    def set_unresponsive_agents_stop_time(self):
        current_time = datetime.now(tz=timezone.utc)

        running_agents = self._agent_repository.get_running_agents()
        self._clean_latest_heartbeats(running_agents)

        for agent in running_agents:
            latest_heartbeat = self._latest_heartbeats.get(agent.id, agent.start_time)

            if (current_time - latest_heartbeat).total_seconds() >= self._heartbeat_timeout:
                logger.warning(
                    f"The last hearbeat from {agent.id} was received at {latest_heartbeat} "
                    "-- marking the agent as stopped"
                )
                agent.stop_time = latest_heartbeat
                self._agent_repository.upsert_agent(agent)
                self._island_event_queue.publish(
                    IslandEventTopic.AGENT_TIMED_OUT, agent_id=agent.id
                )

    def _clean_latest_heartbeats(self, running_agents: Sequence[Agent]):
        # If an agent is no longer running, then we no longer need to store its most recent
        # heartbeat

        running_agent_ids = {agent.id for agent in running_agents}
        self._latest_heartbeats = {
            agent_id: heartbeat_timestamp
            for agent_id, heartbeat_timestamp in self._latest_heartbeats.items()
            if agent_id in running_agent_ids
        }
