import logging
from http import HTTPStatus
from json import JSONDecodeError

from flask import request

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services import AgentSignalsService

logger = logging.getLogger(__name__)


class AgentSignals(AbstractResource):
    urls = ["/api/agent-signals/terminate-all", "/api/agent-signals/<string:agent_id>"]

    def __init__(
        self,
        island_event_queue: IIslandEventQueue,
        agent_signals_service: AgentSignalsService,
    ):
        self._island_event_queue = island_event_queue
        self._agent_signals_service = agent_signals_service

    def post(self):
        try:
            terminate_timestamp = request.json["kill_time"]
            if terminate_timestamp is None:
                raise ValueError("Terminate signal's timestamp is empty")

            self._island_event_queue.publish(
                IslandEventTopic.TERMINATE_AGENTS, timestamp=terminate_timestamp
            )

        except (JSONDecodeError, TypeError, ValueError, KeyError) as err:
            return {"error": err}, HTTPStatus.BAD_REQUEST

        return {}, HTTPStatus.NO_CONTENT

    def get(self, agent_id: str):
        agent_signals = self._agent_signals_service.get_signals(agent_id)
        return agent_signals.dict(), HTTPStatus.OK
