import json

from flask import make_response, request

from common.agent_configuration.agent_configuration import (
    AgentConfiguration as AgentConfigurationObject,
)
from monkey_island.cc.repositories import (
    IAgentConfigurationRepository,
    PluginConfigurationValidationError,
)
from monkey_island.cc.resources.AbstractResource import AbstractResource


class AgentConfiguration(AbstractResource):
    urls = ["/api/agent-configuration"]

    def __init__(self, agent_configuration_repository: IAgentConfigurationRepository):
        self._agent_configuration_repository = agent_configuration_repository

    # Used by the agent. Can't secure
    def get(self):
        configuration = self._agent_configuration_repository.get_configuration()
        configuration_dict = configuration.dict(simplify=True)
        return make_response(configuration_dict, 200)

    def put(self):
        try:
            configuration_object = AgentConfigurationObject(**request.json)
            self._agent_configuration_repository.update_configuration(configuration_object)
            # API Spec: Should return 204 (NO CONTENT)
            return make_response({}, 200)
        except (
            ValueError,
            TypeError,
            json.JSONDecodeError,
            PluginConfigurationValidationError,
        ) as err:

            return make_response(
                {"error": f"Invalid configuration supplied: {err}"},
                400,
            )
