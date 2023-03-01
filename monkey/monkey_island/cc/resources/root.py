import logging
from http import HTTPStatus

from flask import request

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import IAgentRepository

logger = logging.getLogger(__name__)


class Root(AbstractResource):
    urls = ["/api"]

    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository

    def get(self, action=None):
        if not action:
            action = request.args.get("action")

        if not action:
            return {}, HTTPStatus.NO_CONTENT
        elif action == "is-up":
            return {"is-up": True}
        else:
            return {"error": "unknown action"}, HTTPStatus.BAD_REQUEST
