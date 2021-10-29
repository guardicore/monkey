import json
import logging

import flask_restful
from flask import make_response, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config_manipulator import update_config_on_mode_set
from monkey_island.cc.services.mode.island_mode_service import ModeNotSetError, get_mode, set_mode
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

logger = logging.getLogger(__name__)


class IslandMode(flask_restful.Resource):
    @jwt_required
    def post(self):
        try:
            body = json.loads(request.data)
            mode_str = body.get("mode")

            mode = IslandModeEnum(mode_str)
            set_mode(mode)

            if not update_config_on_mode_set(mode):
                logger.error(
                    "Could not apply configuration changes per mode. "
                    "Using default advanced configuration."
                )

            return make_response({}, 200)
        except (AttributeError, json.decoder.JSONDecodeError):
            return make_response({}, 400)
        except ValueError:
            return make_response({}, 422)

    @jwt_required
    def get(self):
        try:
            island_mode = get_mode()
            return make_response({"mode": island_mode}, 200)

        except ModeNotSetError:
            return make_response({"mode": None}, 200)
