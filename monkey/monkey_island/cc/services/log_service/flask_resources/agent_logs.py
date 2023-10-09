import logging
from http import HTTPStatus

from flask import request
from flask_security import auth_token_required, roles_accepted
from monkeytypes import AgentID

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import UnknownRecordError
from monkey_island.cc.services.authentication_service import AccountRole

from ..i_agent_log_repository import IAgentLogRepository

logger = logging.getLogger(__name__)


class AgentLogs(AbstractResource):
    urls = ["/api/agent-logs/<uuid:agent_id>"]

    def __init__(self, agent_log_repository: IAgentLogRepository):
        self._agent_log_repository = agent_log_repository

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self, agent_id: AgentID):
        try:
            log_contents = self._agent_log_repository.get_agent_log(agent_id)
        except UnknownRecordError as err:
            logger.error(f"No log found for agent {agent_id}: {err}")
            return "", HTTPStatus.NOT_FOUND

        return log_contents, HTTPStatus.OK

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name)
    def put(self, agent_id: AgentID):
        log_contents = request.json

        self._agent_log_repository.upsert_agent_log(agent_id, log_contents)

        return {}, HTTPStatus.NO_CONTENT
