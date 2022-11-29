from datetime import datetime
from threading import Lock
from typing import Dict, Optional

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
        self._last_agent_heartbeats: Dict[AgentID, Optional[datetime]] = {}
        self._lock: Lock = Lock()

    def update_agent_last_heartbeat(self, agent_id: AgentID, timestamp: Optional[datetime]):
        with self._lock:
            self._last_agent_heartbeats[agent_id] = timestamp
