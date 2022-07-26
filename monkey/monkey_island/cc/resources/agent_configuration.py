import json

from flask import make_response, request

from common.agent_configuration.agent_configuration import (
    AgentConfiguration as AgentConfigurationObject,
)
from common.agent_configuration.agent_configuration import InvalidConfigurationError
from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class AgentConfiguration(AbstractResource):
    urls = ["/api/agent-configuration"]

    def __init__(self, agent_configuration_repository: IAgentConfigurationRepository):
        self._agent_configuration_repository = agent_configuration_repository

    # Used by the agent. Can't secure
    def get(self):
        configuration = self._agent_configuration_repository.get_configuration()
        configuration_json = AgentConfigurationObject.to_json(configuration)
        return make_response(configuration_json, 200)

    @jwt_required
    def post(self):
        try:
            configuration_object = AgentConfigurationObject.from_mapping(request.json)
            self._agent_configuration_repository.store_configuration(configuration_object)
            # API Spec: Should return 204 (NO CONTENT)
            return make_response({}, 200)
        except (InvalidConfigurationError, json.JSONDecodeError) as err:
            return make_response(
                {"error": f"Invalid configuration supplied: {err}"},
                400,
            )
