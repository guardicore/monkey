from enum import Enum
from flask import jsonify, request

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.repository import FileAgentConfigurationRepository

class ConfigurationTypeEnum(Enum):
    ISLAND = "island"
    AGENT = "agent"


class Configuration(AbstractResource):
    urls = ["/api/configuration/<string:configuration_type>"]

    @jwt_required
    def get(self, configuration_type: str):
        # we probably still need this because of credential fields, HTTP ports, etc in the config?
        if configuration_type == ConfigurationTypeEnum.ISLAND:
            pass
        elif configuration_type == ConfigurationTypeEnum.AGENT:
            configuration = FileAgentConfigurationRepository.get_configuration()
            return jsonify(configuration=configuration)

    @jwt_required
    def post(self):
        pass

    @jwt_required
    def patch(self):  # reset the config here?
        pass
