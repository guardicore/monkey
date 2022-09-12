from http import HTTPStatus

from flask import make_response

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class ResetAgentConfiguration(AbstractResource):
    urls = ["/api/reset-agent-configuration"]

    def __init__(self, event_queue: IIslandEventQueue):
        self._event_queue = event_queue

    @jwt_required
    def post(self):
        """
        Reset the agent configuration to its default values
        """
        self._event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)

        return make_response({}, HTTPStatus.OK)
