import json

import marshmallow
from flask import jsonify, make_response, request

from common.configuration.agent_configuration import AgentConfigurationSchema
from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class AgentConfiguration(AbstractResource):
    urls = ["/api/agent-configuration"]

    def __init__(self, agent_configuration_repository: IAgentConfigurationRepository):
        self._agent_configuration_repository = agent_configuration_repository
        self._schema = AgentConfigurationSchema()

    @jwt_required
    def get(self):
        configuration = self._agent_configuration_repository.get_configuration()
        configuration_json = self._schema.dumps(configuration)
        return jsonify(configuration_json=configuration_json)

    @jwt_required
    def post(self):
        request_contents = json.loads(request.data)
        configuration_json = json.loads(request_contents["config"])

        try:
            configuration_object = self._schema.load(configuration_json)
            self._agent_configuration_repository.store_configuration(configuration_object)
            return make_response({}, 200)
        except marshmallow.exceptions.ValidationError:
            return make_response(
                {
                    "message": "Invalid configuration supplied. "
                    "Maybe the format is outdated or the file has been corrupted."
                },
                400,
            )
