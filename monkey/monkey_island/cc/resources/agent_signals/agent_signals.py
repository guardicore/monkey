import logging
from http import HTTPStatus

from flask_security import auth_token_required, roles_accepted
from monkeytypes import AgentID

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services import AgentSignalsService
from monkey_island.cc.services.authentication_service import AccountRole

logger = logging.getLogger(__name__)


class AgentSignals(AbstractResource):
    urls = ["/api/agent-signals/<uuid:agent_id>"]

    def __init__(
        self,
        agent_signals_service: AgentSignalsService,
    ):
        self._agent_signals_service = agent_signals_service

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name)
    def get(self, agent_id: AgentID):
        agent_signals = self._agent_signals_service.get_signals(agent_id)
        return agent_signals.to_json_dict(), HTTPStatus.OK
