import json
from dataclasses import dataclass
from itertools import chain
from typing import Mapping

import marshmallow
from flask import jsonify, request

from common.configuration.agent_configuration import AgentConfigurationSchema
from common.configuration.default_agent_configuration import DEFAULT_AGENT_CONFIGURATION
from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class ImportStatuses:
    INVALID_CONFIGURATION = "invalid_configuration"
    IMPORTED = "imported"


@dataclass
class ResponseContents:
    import_status: str = ImportStatuses.IMPORTED
    message: str = ""
    status_code: int = 200

    def form_response(self):
        return self.__dict__


class AgentConfiguration(AbstractResource):
    urls = ["/api/agent-configuration"]

    def __init__(self, agent_configuration_repository: IAgentConfigurationRepository):
        self._agent_configuration_repository = agent_configuration_repository
        self._schema = AgentConfigurationSchema()

    @jwt_required
    def get(self):
        configuration = self._agent_configuration_repository.get_configuration()
        configuration_json = self._schema.dumps(configuration)
        # for when the agent requests the config; it needs the exploiters' metadata
        # Q: but this'll cause issues when the frontend requests the config?
        AgentConfiguration._add_metadata_to_config(configuration_json)
        return jsonify(configuration_json=configuration_json)

    @staticmethod
    def _add_metadata_to_config(configuration_json):
        for exploiter_type in ["brute_force", "vulnerability"]:
            for exploiter in configuration_json["propagation"]["exploitation"][exploiter_type]:
                # there has to be a better way to do this
                if "supported_os" not in exploiter:
                    exploiter["supported_os"] = DEFAULT_AGENT_CONFIGURATION["propagation"][
                        "exploitation"
                    ][exploiter_type]["supported_os"]

    @jwt_required
    def post(self):
        request_contents = json.loads(request.data)
        configuration_json = json.loads(request_contents["config"])
        AgentConfiguration._remove_metadata_from_config(configuration_json)

        try:
            configuration_object = self._schema.loads(configuration_json)
            self._agent_configuration_repository.store_configuration(configuration_object)
            return ResponseContents().form_response()
        except marshmallow.exceptions.ValidationError:
            return ResponseContents(
                import_status=ImportStatuses.INVALID_CONFIGURATION,
                message="Invalid configuration supplied. "
                "Maybe the format is outdated or the file has been corrupted.",
                status_code=400,
            ).form_response()

    @staticmethod
    def _remove_metadata_from_config(configuration_json: Mapping):
        for exploiter in chain(
            configuration_json["propagation"]["exploitation"]["brute_force"],
            configuration_json["propagation"]["exploitation"]["vulnerability"],
        ):
            if "supported_os" in exploiter:
                del exploiter["supported_os"]
