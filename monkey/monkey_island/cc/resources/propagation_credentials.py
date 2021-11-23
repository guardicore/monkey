import flask_restful

from monkey_island.cc.services.config import ConfigService


class PropagationCredentials(flask_restful.Resource):
    def get(self):

        return {"propagation_credentials": ConfigService.get_config_propagation_credentials()}
