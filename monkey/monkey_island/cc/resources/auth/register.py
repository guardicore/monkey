import logging
from http import HTTPStatus

from flask import make_response, request
from flask_security.views import register

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

logger = logging.getLogger(__name__)


class Register(AbstractResource):
    """
    A resource for user registration
    """

    urls = ["/api/register"]

    def __init__(
        self,
        repository_encryptor: ILockableEncryptor,
        island_event_queue: IIslandEventQueue,
    ):
        self._repository_encryptor = repository_encryptor
        self._island_event_queue = island_event_queue

    def post(self):
        """
        Registers a new user using flask security register

        """
        username, password = get_username_password_from_request(request)

        try:
            # This method take the request data and pass it to the RegisterForm
            # where a registration request is preform. Return value is a flask.Response
            # object
            response = register()

            if response.status_code == HTTPStatus.OK:
                self._island_event_queue.publish(IslandEventTopic.CLEAR_SIMULATION_DATA)
                self._island_event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)
                self._island_event_queue.publish(
                    topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET
                )

                self._reset_repository_encryptor(username, password)

            return make_response(response)
        except Exception as err:
            return make_response({"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _reset_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.reset_key()
        self._repository_encryptor.unlock(secret.encode())


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
