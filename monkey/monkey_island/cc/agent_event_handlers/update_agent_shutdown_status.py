import logging
from datetime import datetime

from common.agent_events import AbstractAgentEvent
from monkey_island.cc.repository import IAgentRepository

logger = logging.getLogger(__name__)


class update_agent_shutdown_status:
    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository

    def __call__(self, event: AbstractAgentEvent):
        agent_id = event.source
        agent = self._agent_repository.get_agent_by_id(agent_id)
        agent.stop_time = datetime.utcfromtimestamp(event.timestamp)
        self._agent_repository.upsert_agent(agent)
