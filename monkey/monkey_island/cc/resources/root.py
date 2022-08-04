import logging

from flask import jsonify, make_response, request

from monkey_island.cc.database import mongo
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.infection_lifecycle import get_completed_steps
from monkey_island.cc.services.utils.network_utils import get_local_ip_addresses

logger = logging.getLogger(__name__)


class Root(AbstractResource):

    urls = ["/api"]

    def get(self, action=None):
        if not action:
            action = request.args.get("action")

        if not action:
            return self.get_server_info()
        elif action == "is-up":
            return {"is-up": True}
        else:
            return make_response(400, {"error": "unknown action"})

    @jwt_required
    def get_server_info(self):
        return jsonify(
            ip_addresses=get_local_ip_addresses(),
            mongo=str(mongo.db),
            completed_steps=get_completed_steps(),
        )
