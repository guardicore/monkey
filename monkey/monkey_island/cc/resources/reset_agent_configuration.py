from http import HTTPStatus

from flask import make_response

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services import RepositoryService


class ResetAgentConfiguration(AbstractResource):
    urls = ["/api/reset-agent-configuration"]

    def __init__(self, repository_service: RepositoryService):
        self._repository_service = repository_service

    @jwt_required
    def post(self):
        """
        Reset the agent configuration to its default values
        """
        self._repository_service.reset_agent_configuration()

        return make_response({}, HTTPStatus.OK)
