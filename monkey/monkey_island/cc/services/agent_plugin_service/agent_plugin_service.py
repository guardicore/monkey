import io
import logging
from threading import Lock
from typing import Any, Dict, List

import requests
import yaml

from common import OperatingSystem
from common.agent_plugins import (
    AgentPlugin,
    AgentPluginManifest,
    AgentPluginMetadata,
    AgentPluginRepositoryIndex,
    AgentPluginType,
    PluginName,
    PluginVersion,
)
from common.decorators import request_cache
from common.utils.file_utils import get_binary_io_sha256_hash
from monkey_island.cc import Version
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.repositories import RetrievalError

from . import IAgentPluginService
from .errors import PluginInstallationError, PluginUninstallationError
from .i_agent_plugin_repository import IAgentPluginRepository
from .plugin_archive_parser import parse_plugin

AGENT_PLUGIN_REPOSITORY_DEVELOP_URL = "https://monkey-plugins-develop.s3.amazonaws.com"
AGENT_PLUGIN_REPOSITORY_RELEASE_2_3_0_URL = "https://s3.amazonaws.com/monkey-plugins-release-2.3.0"
INDEX_FILE_NAME = "index.yml"

PLUGIN_TTL = 60 * 60  # if the index is older then hour we refresh the index

logger = logging.getLogger(__name__)


class AgentPluginService(IAgentPluginService):
    """
    A service for retrieving and manipulating Agent plugins
    """

    def __init__(
        self,
        agent_plugin_repository: IAgentPluginRepository,
        version: Version,
    ):
        self._agent_plugin_repository = agent_plugin_repository
        self._lock = Lock()

        self._plugin_repository_url = AGENT_PLUGIN_REPOSITORY_RELEASE_2_3_0_URL
        if version.deployment == Deployment.DEVELOP:
            self._plugin_repository_url = AGENT_PLUGIN_REPOSITORY_DEVELOP_URL

        logger.info(f"Agent plugins will be downloaded from {self._plugin_repository_url}")

        # Since the request_cache decorator maintains state, we must decorate the method in the
        # constructor, otherwise all instances of this class will share the same cache.
        self._download_index = request_cache(PLUGIN_TTL)(self._download_index)  # type: ignore [assignment]  # noqa: E501

    def get_plugin(
        self,
        host_operating_system: OperatingSystem,
        plugin_type: AgentPluginType,
        plugin_name: PluginName,
    ) -> AgentPlugin:
        return self._agent_plugin_repository.get_plugin(
            host_operating_system, plugin_type, plugin_name
        )

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, Dict[str, Any]]]:
        return self._agent_plugin_repository.get_all_plugin_configuration_schemas()

    def get_all_plugin_manifests(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, AgentPluginManifest]]:
        return self._agent_plugin_repository.get_all_plugin_manifests()

    def install_plugin_archive(self, agent_plugin_archive: bytes):
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

    def install_plugin_from_repository(
        self, plugin_type: AgentPluginType, plugin_name: PluginName, plugin_version: PluginVersion
    ):
        plugin_metadata = self._find_plugin_in_repository(plugin_type, plugin_name, plugin_version)

        plugin_download_url = self._get_file_download_url(plugin_metadata=plugin_metadata)
        response = requests.get(plugin_download_url)
        plugin_archive = response.content
        if not self._validate_plugin_hash(plugin_metadata, plugin_archive):
            raise PluginInstallationError(
                f'Error occured installing plugin with type "{plugin_type}", name "{plugin_name}",'
                f' and version "{plugin_version}" from plugin repository: Invalid hashes.'
            )

        self.install_plugin_archive(plugin_archive)

    def _find_plugin_in_repository(
        self, plugin_type: AgentPluginType, plugin_name: PluginName, plugin_version: PluginVersion
    ) -> AgentPluginMetadata:
        plugin_repository_index = self.get_available_plugins()
        available_versions_of_plugin: List[
            AgentPluginMetadata
        ] = plugin_repository_index.plugins.get(plugin_type.value, {}).get(plugin_name, [])
        for plugin_metadata in available_versions_of_plugin:
            if plugin_metadata.version == plugin_version:
                return plugin_metadata

        raise PluginInstallationError(
            f'Could not find plugin with type "{plugin_type}", name "{plugin_name}", and '
            f'version "{plugin_version}" in plugin repository'
        )

    def _get_file_download_url(self, plugin_metadata: AgentPluginMetadata) -> str:
        plugin_file_path = plugin_metadata.resource_path
        return f"{self._plugin_repository_url}/{plugin_file_path}"

    def _validate_plugin_hash(
        self, plugin_metadata: AgentPluginMetadata, plugin_archive: bytes
    ) -> bool:
        plugin_hash = plugin_metadata.sha256
        plugin_archive_hash = get_binary_io_sha256_hash(io.BytesIO(plugin_archive))

        return plugin_hash == plugin_archive_hash

    def get_available_plugins(self, force_refresh: bool = False) -> AgentPluginRepositoryIndex:
        if force_refresh:
            self._download_index.clear_cache()  # type: ignore [attr-defined]

        return self._download_index()

    # This method is decorated in __init__() to cache responses
    def _download_index(self) -> AgentPluginRepositoryIndex:
        try:
            response = requests.get(f"{self._plugin_repository_url}/{INDEX_FILE_NAME}")
            repository_index_yml = yaml.safe_load(response.text)

            return AgentPluginRepositoryIndex(**repository_index_yml)
        except Exception as err:
            raise RetrievalError("Failed to get agent plugin repository index") from err

    def uninstall_plugin(self, plugin_type: AgentPluginType, plugin_name: PluginName):
        try:
            self._agent_plugin_repository.remove_agent_plugin(
                agent_plugin_type=plugin_type, agent_plugin_name=plugin_name
            )
        except Exception as err:
            raise PluginUninstallationError(
                f"Failed to uninstall the plugin {plugin_name} of type {plugin_type}: {err}"
            )
