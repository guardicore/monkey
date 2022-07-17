import json
import logging

from flask import make_response, request

from monkey_island.cc.models import IslandMode as IslandModeEnum
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services import IslandModeService

logger = logging.getLogger(__name__)


class IslandMode(AbstractResource):
    # API Spec: Instead of POST, this could just be PATCH
    urls = ["/api/island-mode"]

    def __init__(self, island_mode_service: IslandModeService):
        self._island_mode_service = island_mode_service

    @jwt_required
    def put(self):
        try:
            body = json.loads(request.data)
            mode = IslandModeEnum(body.get("mode"))

            self._island_mode_service.set_mode(mode)

            return make_response({}, 200)
        except (AttributeError, json.decoder.JSONDecodeError):
            return make_response({}, 400)
        except ValueError:
            return make_response({}, 422)

    @jwt_required
    def get(self):
        island_mode = self._island_mode_service.get_mode()
        return make_response({"mode": island_mode.value}, 200)
