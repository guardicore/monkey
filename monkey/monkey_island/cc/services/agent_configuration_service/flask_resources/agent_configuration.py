import json
from http import HTTPStatus

from flask import make_response, request
from flask_security import auth_token_required, roles_accepted

from common.agent_configuration.agent_configuration import (
    AgentConfiguration as AgentConfigurationObject,
)
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentConfigurationService, PluginConfigurationValidationError


class AgentConfiguration(AbstractResource):
    urls = ["/api/agent-configuration"]

    def __init__(self, agent_configuration_service: IAgentConfigurationService):
        self._agent_configuration_service = agent_configuration_service

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name, AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        configuration = self._agent_configuration_service.get_configuration()
        configuration_dict = configuration.to_json_dict()
        return make_response(configuration_dict, HTTPStatus.OK)

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def put(self):
        try:
            configuration_object = AgentConfigurationObject(**request.json)
            self._agent_configuration_service.update_configuration(configuration_object)
            return make_response({}, HTTPStatus.NO_CONTENT)
        except (
            ValueError,
            TypeError,
            json.JSONDecodeError,
            PluginConfigurationValidationError,
        ) as err:
            return make_response(
                {"error": f"Invalid configuration supplied: {err}"},
                HTTPStatus.BAD_REQUEST,
            )
