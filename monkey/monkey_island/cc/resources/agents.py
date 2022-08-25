import json
import logging
from http import HTTPStatus

from flask import make_response, request

from common import AgentRegistrationData
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class Agents(AbstractResource):
    urls = ["/api/agents"]

    def post(self):
        try:
            # Just parse for now
            agent_registration_data = AgentRegistrationData(**request.json)

            logger.debug(f"Agent registered: {agent_registration_data}")

            return make_response({}, HTTPStatus.NO_CONTENT)
        except (TypeError, ValueError, json.JSONDecodeError) as err:
            return make_response(
                {"error": f"Invalid configuration supplied: {err}"},
                HTTPStatus.BAD_REQUEST,
            )
