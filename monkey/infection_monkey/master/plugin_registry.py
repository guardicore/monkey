import logging
from pathlib import Path
from tarfile import TarFile
from typing import Any

from serpentarium import PluginLoader

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import IIslandAPIClient

logger = logging.getLogger()


def check_safe_archive(dest_path: Path, archive: TarFile) -> bool:
    path = Path.resolve(dest_path)
    for name in archive.getnames():
        if path not in Path.resolve(dest_path / name).parents:
            return False
    return True


def extract_plugin(data: bytes, dest_path: Path):
    archive = TarFile(data, "r")
    if not check_safe_archive(dest_path, archive):
        raise ValueError("Unsafe archive")

    archive.extractall(dest_path)  # noqa: DUO115


class PluginRegistry:
    def __init__(self, island_api_client: IIslandAPIClient, plugin_loader: PluginLoader):
        """
        `self._registry` looks like -
            {
                AgentPluginType.EXPLOITER: {
                    "ZerologonExploiter": ZerologonExploiter,
                    "SMBExploiter": SMBExploiter
                }
            }
        """
        self._registry = {}
        self._island_api_client = island_api_client
        self._plugin_loader = plugin_loader

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: AgentPluginType) -> None:
        self._registry.setdefault(plugin_type, {})
        self._registry[plugin_type][plugin_name] = plugin

        logger.debug(f"Plugin '{plugin_name}' loaded")

    def get_plugin(self, plugin_name: str, plugin_type: AgentPluginType) -> Any:
        try:
            plugin = self._registry[plugin_type][plugin_name]
        except KeyError:
            response = self._island_api_client.get_plugin(plugin_type, plugin_name)
            if 400 <= response.status_code < 500:
                raise UnknownPluginError(
                    f"Unknown plugin '{plugin_name}' of type '{plugin_type.value}'"
                )
            elif 200 <= response.status_code < 300:
                raise NotImplementedError()
            else:
                raise Exception(
                    f"Unexpected response status code {response.status} received while fetching "
                    f"plugin '{plugin_name}' of type '{plugin_type.value}' from Island"
                )

        logger.debug(f"Plugin '{plugin_name}' found")

        return plugin
