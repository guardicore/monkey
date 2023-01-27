import logging
import threading
from typing import Mapping, Optional

from common.agent_plugins import AgentPluginManifest, AgentPluginType
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError
from infection_monkey.model import TargetHost

logger = logging.getLogger(__name__)


class PluginCompatabilityVerifier:
    """
    Verify plugin compatibility to run
    """

    def __init__(
        self,
        island_api_client: IIslandAPIClient,
        exploiter_plugin_manifests: Mapping[str, AgentPluginManifest],
    ):
        self._island_api_client = island_api_client
        self._exploiter_plugin_manifests = dict(exploiter_plugin_manifests)
        self._cache_lock = threading.Lock()

    def verify_exploiter_compatibility(self, exploiter_name: str, target_host: TargetHost) -> bool:
        """
        Verify exploiter compatibility to run on a target host

        :param exploiter_name: Name of the exploiter
        :param target_host: Target host
        """
        exploiter_plugin_manifest = self._get_exploiter_plugin_manifest(exploiter_name)
        if exploiter_plugin_manifest is None:
            return False

        return (
            target_host.operating_system is None
            or target_host.operating_system in exploiter_plugin_manifest.target_operating_systems
        )

    def _get_exploiter_plugin_manifest(self, exploiter_name: str) -> Optional[AgentPluginManifest]:
        """
        Get exploiter plugin manifest

        Request island for plugin manifest if it doesn't exists and return it
        :param exploiter_name: Name of exploiter
        """
        with self._cache_lock:
            if exploiter_name in self._exploiter_plugin_manifests:
                return self._exploiter_plugin_manifests[exploiter_name]

            try:
                plugin_manifest = self._island_api_client.get_agent_plugin_manifest(
                    AgentPluginType.EXPLOITER, exploiter_name
                )
                self._exploiter_plugin_manifests[exploiter_name] = plugin_manifest

                return plugin_manifest
            except IslandAPIError:
                logger.exception(f"No plugin manifest found for {exploiter_name}")

            return None
