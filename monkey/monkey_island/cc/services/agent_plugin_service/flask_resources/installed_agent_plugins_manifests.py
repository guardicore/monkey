import logging
from http import HTTPStatus

from flask import make_response
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import UnknownRecordError
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService

logger = logging.getLogger(__name__)


class InstalledAgentPluginsManifests(AbstractResource):
    urls = ["/api/agent-plugins/installed/manifests"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        """
        Get manifests of all installed plugins
        """
        try:
            installed_agent_plugins_manifests = (
                self._agent_plugin_service.get_all_plugin_manifests()
            )
            return make_response(
                installed_agent_plugins_manifests.dict(simplify=True), HTTPStatus.OK
            )
        except UnknownRecordError:
            message = "Could not retrieve manifests for installed plugins"
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.INTERNAL_SERVER_ERROR)
