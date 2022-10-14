import logging

from flask import make_response, request

from monkey_island.cc.repository import IAgentRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class Root(AbstractResource):
    urls = ["/api"]

    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository

    def get(self, action=None):
        if not action:
            action = request.args.get("action")

        if not action:
            return make_response(204)
        elif action == "is-up":
            return {"is-up": True}
        else:
            return make_response(400, {"error": "unknown action"})
