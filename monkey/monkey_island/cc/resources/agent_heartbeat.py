import time
from http import HTTPStatus
from json import JSONDecodeError

from flask import request

from common.types import AgentID
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.resources.AbstractResource import AbstractResource


class AgentHeartbeat(AbstractResource):
    urls = ["/api/agent/<uuid:agent_id>/heartbeat"]

    def __init__(self, island_event_queue: IIslandEventQueue):
        self._island_event_queue = island_event_queue

    # Used by the agent. Can't secure.
    def post(self, agent_id: AgentID):
        try:
            heartbeat_timestamp = request.json["heartbeat_timestamp"]
            if heartbeat_timestamp is None:
                heartbeat_timestamp = time.time()
            elif heartbeat_timestamp <= 0:
                raise ValueError("Terminate signal's timestamp is not a positive integer")

            self._island_event_queue.publish(
                IslandEventTopic.AGENT_HEARTBEAT, agent_id=agent_id, timestamp=heartbeat_timestamp
            )

            return {}, HTTPStatus.NO_CONTENT

        except (JSONDecodeError, TypeError, ValueError, KeyError) as err:
            return {"error": err}, HTTPStatus.BAD_REQUEST
