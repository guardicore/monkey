import logging
from http import HTTPStatus

from flask import make_response, request
from flask_security import auth_token_required, roles_accepted
from monkeytypes import OperatingSystem

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentBinaryService

logger = logging.getLogger(__name__)


class AgentBinariesMasque(AbstractResource):
    urls = ["/api/agent-binaries/<string:os>/masque"]

    def __init__(self, agent_binary_service: IAgentBinaryService):
        self._agent_binary_service = agent_binary_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self, os):
        try:
            operating_system = OperatingSystem[os.upper()]
        except KeyError as err:
            message = f'Could not get masque for OS "{os}": {err}'
            logger.error(message)
            return make_response({"error": message}, HTTPStatus.NOT_FOUND)

        masque = self._agent_binary_service.get_masque(operating_system)
        masque = b"" if masque is None else masque

        return make_response(masque, HTTPStatus.OK, {"Content-Type": "application/octet-stream"})

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def put(self, os):
        masque = request.data
        masque = None if len(masque) == 0 else masque

        try:
            operating_system = OperatingSystem[os.upper()]
        except KeyError as err:
            message = f'Could not set masque for OS "{os}": {err}'
            logger.error(message)
            return make_response({"error": message}, HTTPStatus.NOT_FOUND)

        self._agent_binary_service.set_masque(operating_system, masque)
        return make_response({}, HTTPStatus.NO_CONTENT)
