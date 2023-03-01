from http import HTTPStatus
from json import JSONDecodeError

from flask import request

from common import AgentHeartbeat as AgentHeartbeatObject
from common.types import AgentID
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.flask_utils import AbstractResource


class AgentHeartbeat(AbstractResource):
    urls = ["/api/agent/<uuid:agent_id>/heartbeat"]

    def __init__(self, island_event_queue: IIslandEventQueue):
        self._island_event_queue = island_event_queue

    # Used by the agent. Can't secure.
    def post(self, agent_id: AgentID):
        try:
            heartbeat = AgentHeartbeatObject(**request.json)

            self._island_event_queue.publish(
                IslandEventTopic.AGENT_HEARTBEAT, agent_id=agent_id, heartbeat=heartbeat
            )

            return {}, HTTPStatus.NO_CONTENT

        except (JSONDecodeError, TypeError, ValueError, KeyError) as err:
            return {"error": err}, HTTPStatus.BAD_REQUEST
