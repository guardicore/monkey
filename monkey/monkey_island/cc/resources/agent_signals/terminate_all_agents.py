import logging
from http import HTTPStatus
from json import JSONDecodeError

from flask import request
from flask_security import auth_token_required, roles_required

from common import AccountRoles
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.models import TerminateAllAgents as TerminateAllAgentsObject

logger = logging.getLogger(__name__)


class TerminateAllAgents(AbstractResource):
    urls = ["/api/agent-signals/terminate-all-agents"]

    def __init__(
        self,
        island_event_queue: IIslandEventQueue,
    ):
        self._island_event_queue = island_event_queue

    @auth_token_required
    @roles_required(AccountRoles.ISLAND.name)
    def post(self):
        try:
            terminate_all_agents = TerminateAllAgentsObject(**request.json)

            self._island_event_queue.publish(
                IslandEventTopic.TERMINATE_AGENTS, terminate_all_agents=terminate_all_agents
            )

        except (JSONDecodeError, TypeError, ValueError, KeyError) as err:
            return {"error": err}, HTTPStatus.BAD_REQUEST

        return {}, HTTPStatus.NO_CONTENT
