from http import HTTPStatus

from flask import make_response

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class ClearSimulationData(AbstractResource):
    urls = ["/api/clear-simulation-data"]

    def __init__(self, island_event_queue: IIslandEventQueue):
        self._island_event_queue = island_event_queue

    @jwt_required
    def post(self):
        """
        Clear all data collected during the simulation
        """

        self._island_event_queue.publish(IslandEventTopic.CLEAR_SIMULATION_DATA)
        return make_response({}, HTTPStatus.NO_CONTENT)
