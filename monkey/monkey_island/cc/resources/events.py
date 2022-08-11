import logging
from http import HTTPStatus

from flask import request

from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class Events(AbstractResource):
    urls = ["/api/events"]

    # Agents needs this
    def post(self):
        event = request.json

        logger.info(f"Event: {event}")

        return {}, HTTPStatus.NO_CONTENT
