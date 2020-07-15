import json
import logging

import flask_restful
from flask import request

import monkey_island.cc.environment.environment_singleton as env_singleton

logger = logging.getLogger(__name__)


class Environment(flask_restful.Resource):
    def patch(self):
        env_data = json.loads(request.data)
        if env_data['server_config'] == "standard":
            if env_singleton.env.needs_registration():
                env_singleton.set_to_standard()
                logger.warning("No user registered, Island on standard mode - no credentials required to access.")
        return {}
