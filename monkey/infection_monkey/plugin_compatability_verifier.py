import logging
from typing import Dict

from common import HARD_CODED_EXPLOITER_MANIFESTS
from common.agent_plugins import AgentPluginManifest

from .i_puppet import IncompatibleOperatingSystemError
from .island_api_client import IIslandAPIClient, IslandAPIError
from .model import TargetHost

logger = logging.getLogger(__name__)


class PluginCompatabilityVerifier:
    def __init__(
        self,
        island_api_client: IIslandAPIClient,
        exploiter_plugin_manifests: Dict[str, AgentPluginManifest] = HARD_CODED_EXPLOITER_MANIFESTS,
    ):
        self._island_api_client = island_api_client
        self._exploiter_plugin_manifests = exploiter_plugin_manifests

    def verify_exploiter_compatibility(self, exploiter_name: str, target_host: TargetHost):
        exploiter_agent_plugin_manifest = self._get_exploiter_plugin_manifest(exploiter_name)
        supported_exploiter_os = exploiter_agent_plugin_manifest.supported_operating_systems

        if (
            target_host.operating_system is None
            or target_host.operating_system in supported_exploiter_os
        ):
            return True
        else:
            raise IncompatibleOperatingSystemError(
                f"Incompatible operating system for "
                f"exploiter:{exploiter_name} and "
                f"target_host:{target_host}"
            )

    def _get_exploiter_plugin_manifest(self, exploiter_name: str):
        try:
            return self._island_api_client.get_agent_plugin_manifest(exploiter_name)
        except Exception:
            return self._exploiter_plugin_manifests[exploiter_name]
