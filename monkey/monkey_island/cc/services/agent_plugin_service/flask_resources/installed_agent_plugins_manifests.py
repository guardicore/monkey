import logging
from http import HTTPStatus
from typing import Any, Dict

from flask import make_response
from flask_security import auth_token_required, roles_accepted
from monkeytypes import AgentPluginManifest, AgentPluginType

from common.agent_plugins import PluginName
from monkey_island.cc.flask_utils import AbstractResource
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

        installed_agent_plugins_manifests = self._agent_plugin_service.get_all_plugin_manifests()
        installed_agent_plugins_manifests_simplified = (
            self._simplify_installed_agent_plugins_manifests(installed_agent_plugins_manifests)
        )

        return make_response(installed_agent_plugins_manifests_simplified, HTTPStatus.OK)

    def _simplify_installed_agent_plugins_manifests(
        self, manifests: Dict[AgentPluginType, Dict[PluginName, AgentPluginManifest]]
    ) -> Dict[str, Dict[str, Dict[str, Any]]]:
        simplified: Dict[str, Dict[str, Dict[str, Any]]] = {}
        for plugin_type in manifests:
            simplified[plugin_type.value] = {}
            for plugin_name in manifests[plugin_type]:
                simplified[plugin_type.value][plugin_name] = manifests[plugin_type][
                    plugin_name
                ].dict(simplify=True)

        return simplified
