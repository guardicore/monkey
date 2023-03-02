import logging
from http import HTTPStatus

from flask import request

from common.types import AgentID
from monkey_island.cc.flask_utils import AbstractResource, jwt_required
from monkey_island.cc.repositories import IAgentLogRepository, UnknownRecordError

logger = logging.getLogger(__name__)


class AgentLogs(AbstractResource):
    urls = ["/api/agent-logs/<uuid:agent_id>"]

    def __init__(self, agent_log_repository: IAgentLogRepository):
        self._agent_log_repository = agent_log_repository

    @jwt_required
    def get(self, agent_id: AgentID):
        try:
            log_contents = self._agent_log_repository.get_agent_log(agent_id)
        except UnknownRecordError as err:
            logger.error(f"No log found for agent {agent_id}: {err}")
            return "", HTTPStatus.NOT_FOUND

        return log_contents, HTTPStatus.OK

    def put(self, agent_id: AgentID):
        log_contents = request.json

        self._agent_log_repository.upsert_agent_log(agent_id, log_contents)

        return {}, HTTPStatus.NO_CONTENT
