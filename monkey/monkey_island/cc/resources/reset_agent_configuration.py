from flask import make_response

from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class ResetAgentConfiguration(AbstractResource):
    urls = ["/api/reset-agent-configuration"]

    def __init__(self, agent_configuration_repository: IAgentConfigurationRepository):
        self._agent_configuration_repository = agent_configuration_repository

    @jwt_required
    def post(self):
        """
        Reset the agent configuration to its default values
        """
        self._agent_configuration_repository.reset_to_default()

        return make_response({}, 200)
