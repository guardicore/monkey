import logging

from flask import jsonify, make_response, request

from monkey_island.cc.repository import IAgentRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.infection_lifecycle import is_report_done

logger = logging.getLogger(__name__)


class Root(AbstractResource):
    urls = ["/api"]

    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository

    def get(self, action=None):
        if not action:
            action = request.args.get("action")

        if not action:
            return self.report_generation_status()
        elif action == "is-up":
            return {"is-up": True}
        else:
            return make_response(400, {"error": "unknown action"})

    @jwt_required
    def report_generation_status(self):
        return jsonify(
            report_done=is_report_done(self._agent_repository),
        )
