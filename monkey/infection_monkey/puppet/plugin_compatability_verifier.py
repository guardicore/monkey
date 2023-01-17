import logging
from typing import Dict, Optional

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
        exploiter_plugin_manifests: Dict[str, AgentPluginManifest],
    ):
        self._island_api_client = island_api_client
        self._exploiter_plugin_manifests = exploiter_plugin_manifests

    def verify_exploiter_compatibility(self, exploiter_name: str, target_host: TargetHost) -> bool:
        """
        Verify exploiter compatibility to run on a target host

        :param exploiter_name: Name of the exploiter
        :param target_host: Target host
        """
        exploiter_plugin_manifest = self._get_exploiter_plugin_manifest(exploiter_name)
        if exploiter_plugin_manifest is None:
            return False

        supported_os = exploiter_plugin_manifest.supported_operating_systems

        return target_host.operating_system is None or target_host.operating_system in supported_os

    def _get_exploiter_plugin_manifest(self, exploiter_name: str) -> Optional[AgentPluginManifest]:
        """
        Get exploiter plugin manifest

        Request island for plugin manifest if it doesn't exists and return it
        :param exploiter_name: Name of exploiter
        """
        if exploiter_name not in self._exploiter_plugin_manifests:
            try:
                plugin_manifest = self._island_api_client.get_agent_plugin_manifest(
                    AgentPluginType.EXPLOITER, exploiter_name
                )

                self._exploiter_plugin_manifests[exploiter_name] = plugin_manifest
            except IslandAPIError:
                logger.exception(f"No plugin manifest found for {exploiter_name}")
                return None
        return self._exploiter_plugin_manifests[exploiter_name]
