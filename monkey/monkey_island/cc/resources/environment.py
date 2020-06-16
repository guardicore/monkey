import json

from flask import request
import flask_restful

import monkey_island.cc.environment.environment_singleton as env_singleton


class Environment(flask_restful.Resource):

    def patch(self):
        env_data = json.loads(request.data)
        if env_data['server_config'] == "standard":
            if env_singleton.env.needs_registration():
                env_singleton.set_to_standard()
        return {}
