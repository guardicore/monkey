import json
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from typing import Mapping

from flask import jsonify, request

from common.configuration.agent_configuration import AgentConfigurationSchema
from common.utils.exceptions import InvalidConfigurationError
from monkey_island.cc.repository import FileAgentConfigurationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class ConfigurationTypeEnum(Enum):
    ISLAND = "island"
    AGENT = "agent"


class ImportStatuses:
    UNSAFE_OPTION_VERIFICATION_REQUIRED = "unsafe_options_verification_required"
    INVALID_CONFIGURATION = "invalid_configuration"
    INVALID_CREDENTIALS = "invalid_credentials"
    IMPORTED = "imported"


@dataclass
class ResponseContents:
    import_status: str = ImportStatuses.IMPORTED
    message: str = ""
    status_code: int = 200
    config: str = ""
    config_schema: str = ""

    def form_response(self):
        return self.__dict__


class Configuration(AbstractResource):
    urls = ["/api/configuration/<string:configuration_type>"]

    @jwt_required
    def get(self, configuration_type: str):
        # Q: we probably still need this because of credential fields, HTTP ports, etc in the
        #    config?
        if configuration_type == ConfigurationTypeEnum.ISLAND:
            pass
        elif configuration_type == ConfigurationTypeEnum.AGENT:
            configuration = FileAgentConfigurationRepository.get_configuration()
            return jsonify(configuration=configuration)

    @jwt_required
    def post(self, configuration_type: str):
        request_contents = json.loads(request.data)
        configuration_json = json.loads(request_contents["config"])
        Configuration._remove_metadata_from_config(configuration_json)

        try:
            # Q: encryption is moving to the frontend; also check this in the frontend?
            if request_contents["unsafeOptionsVerified"]:
                schema = AgentConfigurationSchema()
                # Q: in what format/schema are we getting the config from the Island?
                # Q: when does flattening the config go away?
                configuration_object = schema.loads(configuration_json)
                FileAgentConfigurationRepository.store_configuration(
                    configuration_object
                )  # check error handling
                return ResponseContents().form_response()
            else:
                return ResponseContents(
                    config=json.dumps(configuration_json),
                    # Q: do we still need a separate config schema like this?
                    # config_schema=ConfigService.get_config_schema(),
                    import_status=ImportStatuses.UNSAFE_OPTION_VERIFICATION_REQUIRED,
                ).form_response()
        except InvalidConfigurationError:
            return ResponseContents(
                import_status=ImportStatuses.INVALID_CONFIGURATION,
                message="Invalid configuration supplied. "
                "Maybe the format is outdated or the file has been corrupted.",
                status_code=400,
            ).form_response()

    @staticmethod
    # Q: why is this really needed? besides the fact that it just doesn't belong in the config
    #    which is being saved in mongo? if nothing, can't we just wait to change the exploiters
    #    to plugins?
    def _remove_metadata_from_config(configuration_json: Mapping):
        for exploiter in chain(
            configuration_json["propagation"]["exploitation"]["brute_force"],
            configuration_json["propagation"]["exploitation"]["vulnerability"],
        ):
            del exploiter["supported_os"]

    @jwt_required
    def patch(self):  # Q: reset the configuration here? or does that make more sense in delete?
        pass
