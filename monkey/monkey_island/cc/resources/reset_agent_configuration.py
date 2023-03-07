from http import HTTPStatus

from flask import make_response
from flask_security import auth_token_required, roles_required

from common import UserRoles
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.flask_utils import AbstractResource


class ResetAgentConfiguration(AbstractResource):
    urls = ["/api/reset-agent-configuration"]

    def __init__(self, island_event_queue: IIslandEventQueue):
        self._island_event_queue = island_event_queue

    @auth_token_required
    @roles_required(UserRoles.ISLAND.name)
    def post(self):
        """
        Reset the agent configuration to its default values
        """
        self._island_event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)

        return make_response({}, HTTPStatus.OK)
