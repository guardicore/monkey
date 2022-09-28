from http import HTTPStatus

from flask import request

from monkey_island.cc.repository import IAgentLogRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class AgentLogs(AbstractResource):
    urls = ["/api/agent-logs/<string:agent_id>"]

    def __init__(self, agent_log_repository: IAgentLogRepository):
        self._agent_log_repository = agent_log_repository

    @jwt_required
    def get(self, agent_id: str):
        agent_log = self._agent_log_repository.get_agent_log(agent_id)

        return agent_log, HTTPStatus.OK

    def put(self, agent_id: str):
        agent_data = request.json["log_contents"]

        self._agent_log_repository.upsert_agent_log(agent_id, agent_data)

        return {}, HTTPStatus.NO_CONTENT
