import logging
from typing import Dict

from common import HARD_CODED_EXPLOITER_MANIFESTS
from common.agent_plugins import AgentPluginManifest, AgentPluginType

from .i_puppet import IncompatibleOperatingSystemError
from .island_api_client import IIslandAPIClient, IslandAPIError
from .model import TargetHost

logger = logging.getLogger(__name__)


class PluginCompatabilityVerifier:
    """
    Verify plugin compatibility to run
    """

    def __init__(
        self,
        island_api_client: IIslandAPIClient,
        exploiter_plugin_manifests: Dict[str, AgentPluginManifest] = HARD_CODED_EXPLOITER_MANIFESTS,
    ):
        self._island_api_client = island_api_client
        self._exploiter_plugin_manifests = exploiter_plugin_manifests

    def verify_exploiter_compatibility(self, exploiter_name: str, target_host: TargetHost):
        """
        Verify exploiter compatibility to run on a target host

        It verifies based on a target host operating system and exploiter manifest
        supported operating systems.
        :param exploiter_name: Name of the exploiter
        :param target_host: Target host
        :raises IncompatibleOperatingSystemError: If exploiter is not compatible to run
        """
        exploiter_agent_plugin_manifest = self._get_exploiter_plugin_manifest(exploiter_name)
        supported_exploiter_os = exploiter_agent_plugin_manifest.supported_operating_systems

        if (
            target_host.operating_system is None
            or target_host.operating_system in supported_exploiter_os
        ):
            return target_host
        else:
            raise IncompatibleOperatingSystemError(
                f"Incompatible operating system for exploiter:{exploiter_name} and"
                f" target_host:{target_host}"
            )

    def _get_exploiter_plugin_manifest(self, exploiter_name: str) -> AgentPluginManifest:
        """
        Get exploiter plugin manifest

        Request island to find the plugin manifest, if it is not
        successful it looks at the hard coded exploiter manifests.
        :param exploiter_name: Name of exploiter
        """
        try:
            return self._island_api_client.get_agent_plugin_manifest(
                AgentPluginType.EXPLOITER, exploiter_name
            )
        except IslandAPIError:
            return self._exploiter_plugin_manifests[exploiter_name]
