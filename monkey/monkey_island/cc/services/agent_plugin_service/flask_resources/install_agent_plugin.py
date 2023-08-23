import logging
from http import HTTPStatus

from flask import make_response, request
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService
from ..errors import PluginInstallationError

logger = logging.getLogger(__name__)


class InstallAgentPlugin(AbstractResource):
    urls = ["/api/install-agent-plugin"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def put(self):
        """
        Install the plugin archive.
        """
        try:
            self._agent_plugin_service.install_plugin_archive(request.data)
            return make_response({}, HTTPStatus.OK)
        except PluginInstallationError as err:
            return make_response(str(err), HTTPStatus.UNPROCESSABLE_ENTITY)
