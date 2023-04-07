import json
import logging
from http import HTTPStatus

from flask import request
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.models import IslandMode as IslandModeEnum
from monkey_island.cc.repositories import ISimulationRepository
from monkey_island.cc.services.authentication_service import AccountRole

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

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def put(self):
        try:
            mode = IslandModeEnum(request.json)
            self._island_event_queue.publish(topic=IslandEventTopic.SET_ISLAND_MODE, mode=mode)
            return {}, HTTPStatus.NO_CONTENT
        except (AttributeError, json.decoder.JSONDecodeError):
            return responses.make_response_to_invalid_request()
        except ValueError:
            return {}, HTTPStatus.UNPROCESSABLE_ENTITY

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        island_mode = self._simulation_repository.get_mode()
        return island_mode.value, HTTPStatus.OK
