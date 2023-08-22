import io
from threading import Lock
from typing import Any, Dict

import requests
import yaml

from common import OperatingSystem
from common.agent_plugins import (
    AgentPlugin,
    AgentPluginManifest,
    AgentPluginRepositoryIndex,
    AgentPluginType,
)
from common.decorators import request_cache
from monkey_island.cc.repositories import RetrievalError

from . import IAgentPluginService
from .errors import PluginInstallationError
from .i_agent_plugin_repository import IAgentPluginRepository
from .plugin_archive_parser import parse_plugin

AGENT_PLUGIN_REPOSITORY_URL = "https://monkey-plugins-develop.s3.amazonaws.com/index.yml"
PLUGIN_TTL = 60 * 60  # if the index is older then hour we refresh the index


class AgentPluginService(IAgentPluginService):
    """
    A service for retrieving and manipulating Agent plugins
    """

    def __init__(
        self,
        agent_plugin_repository: IAgentPluginRepository,
    ):
        self._agent_plugin_repository = agent_plugin_repository
        self._lock = Lock()

        # Since the request_cache decorator maintains state, we must decorate the method in the
        # constructor, otherwise all instances of this class will share the same cache.
        self._download_index = request_cache(PLUGIN_TTL)(self._download_index)  # type: ignore [assignment]  # noqa: E501

    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        return self._agent_plugin_repository.get_plugin(host_operating_system, plugin_type, name)

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        return self._agent_plugin_repository.get_all_plugin_configuration_schemas()

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        return self._agent_plugin_repository.get_all_plugin_manifests()

    def install_agent_plugin_archive(self, agent_plugin_archive: bytes):
        with self._lock:
            try:
                os_agent_plugins = parse_plugin(io.BytesIO(agent_plugin_archive))
            except ValueError as err:
                raise PluginInstallationError("Failed to install the plugin") from err

            plugin = next(iter(os_agent_plugins.values()))
            self._agent_plugin_repository.remove_agent_plugin(
                agent_plugin_type=plugin.plugin_manifest.plugin_type,
                agent_plugin_name=plugin.plugin_manifest.name,
            )

            for operating_system, agent_plugin in os_agent_plugins.items():
                self._agent_plugin_repository.store_agent_plugin(
                    operating_system=operating_system, agent_plugin=agent_plugin
                )

    def get_available_plugins(self, force_refresh: bool) -> AgentPluginRepositoryIndex:
        if force_refresh:
            self._download_index.clear_cache()  # type: ignore [attr-defined]

        return self._download_index()

    # This method is decorated in __init__() to cache responses
    def _download_index(self) -> AgentPluginRepositoryIndex:
        try:
            response = requests.get(AGENT_PLUGIN_REPOSITORY_URL)
            repository_index_yml = yaml.safe_load(response.text)

            return AgentPluginRepositoryIndex(**repository_index_yml)
        except Exception as err:
            raise RetrievalError("Failed to get agent plugin repository index") from err

    def uninstall_agent_plugin(self, plugin_type: AgentPluginType, name: str):
        self._agent_plugin_repository.remove_agent_plugin(
            agent_plugin_type=plugin_type, agent_plugin_name=name
        )
