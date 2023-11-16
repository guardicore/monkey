import logging
from datetime import datetime

import pytz
from monkeyevents import AbstractAgentEvent

from monkey_island.cc.repositories import IAgentRepository

logger = logging.getLogger(__name__)


class update_agent_shutdown_status:
    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository

    def __call__(self, event: AbstractAgentEvent):
        logger.debug(f"Agent shutdown: {event}")

        agent_id = event.source
        agent = self._agent_repository.get_agent_by_id(agent_id)
        agent.stop_time = datetime.fromtimestamp(event.timestamp, tz=pytz.UTC)
        self._agent_repository.upsert_agent(agent)
