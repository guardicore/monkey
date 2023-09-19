import logging
import threading
from typing import Dict, Optional

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from infection_monkey.i_puppet import TargetHost
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError

logger = logging.getLogger(__name__)


class PluginCompatibilityVerifier:
    """
    Verify plugin compatibility to run
    """

    def __init__(
        self,
        island_api_client: IIslandAPIClient,
        operating_system: OperatingSystem,
    ):
        self._island_api_client = island_api_client
        self._operating_system = operating_system
        self._plugin_manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}
        self._cache_lock = threading.Lock()

    def verify_local_operating_system_compatibility(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> bool:
        plugin_manifest = self._get_plugin_manifest(plugin_type, plugin_name)
        if plugin_manifest is None:
            return False

        return self._operating_system in plugin_manifest.supported_operating_systems

    def verify_target_operating_system_compatibility(
        self, plugin_type: AgentPluginType, plugin_name: str, target_host: TargetHost
    ) -> bool:
        """
        Verify exploiter compatibility to run on a target host

        :param plugin_type: Type of the plugin
        :param plugin_name: Name of the plugin
        :param target_host: Target host
        """
        plugin_manifest = self._get_plugin_manifest(plugin_type, plugin_name)
        if plugin_manifest is None:
            return False

        return (
            target_host.operating_system is None
            or target_host.operating_system in plugin_manifest.target_operating_systems
        )

    def _get_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> Optional[AgentPluginManifest]:
        """
        Get plugin manifest

        Request island for plugin manifest if it doesn't exists and return it
        :param plugin_type: Type of the plugin
        :param plugin_name: Name of the plugin
        """
        plugin_type_manifests = self._plugin_manifests.setdefault(plugin_type, {})
        with self._cache_lock:
            if plugin_name in plugin_type_manifests:
                return plugin_type_manifests[plugin_name]

            try:
                plugin_manifest = self._island_api_client.get_agent_plugin_manifest(
                    plugin_type, plugin_name
                )
                plugin_type_manifests[plugin_name] = plugin_manifest

                return plugin_manifest
            except IslandAPIError:
                logger.exception(f"No plugin manifest found for {plugin_name}")

            return None
