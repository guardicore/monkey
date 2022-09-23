import logging
from http import HTTPStatus

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services import AgentSignalsService

logger = logging.getLogger(__name__)


class AgentSignals(AbstractResource):
    urls = ["/api/agent-signals/<string:agent_id>"]

    def __init__(
        self,
        agent_signals_service: AgentSignalsService,
    ):
        self._agent_signals_service = agent_signals_service

    def get(self, agent_id: str):
        agent_signals = self._agent_signals_service.get_signals(agent_id)
        return agent_signals.dict(simplify=True), HTTPStatus.OK
