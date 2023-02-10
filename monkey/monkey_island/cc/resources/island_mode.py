import json
import logging
from http import HTTPStatus

from flask import request

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode as IslandModeEnum
from monkey_island.cc.repositories import ISimulationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required

logger = logging.getLogger(__name__)


class IslandMode(AbstractResource):
    urls = ["/api/island/mode"]

    def __init__(
        self,
        island_event_queue: IIslandEventQueue,
        simulation_repository: ISimulationRepository,
    ):
        self._island_event_queue = island_event_queue
        self._simulation_repository = simulation_repository

    @jwt_required
    def put(self):
        try:
            mode = IslandModeEnum(request.json)
            self._island_event_queue.publish(topic=IslandEventTopic.SET_ISLAND_MODE, mode=mode)
            return {}, HTTPStatus.NO_CONTENT
        except (AttributeError, json.decoder.JSONDecodeError):
            return {}, HTTPStatus.BAD_REQUEST
        except ValueError:
            return {}, HTTPStatus.UNPROCESSABLE_ENTITY

    @jwt_required
    def get(self):
        island_mode = self._simulation_repository.get_mode()
        return island_mode.value, HTTPStatus.OK
