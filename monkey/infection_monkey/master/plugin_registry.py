import logging
from copy import copy
from pathlib import Path
from tarfile import TarFile
from threading import current_thread
from typing import Any

from serpentarium import PluginLoader

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIRequestError

logger = logging.getLogger()


def check_safe_archive(destination_path: Path, archive: TarFile) -> bool:
    for name in archive.getnames():
        file_path = Path.resolve(destination_path / name)
        # check that the archive has no files whose names start with "/" or ".."
        if destination_path not in file_path.parents:
            return False

    for member in archive.getmembers():
        # check that the file is not a link or device
        if not member.isfile() or not member.isdir():
            return False

    return True


def extract_plugin(data: bytes, destination_path: Path):
    archive = TarFile(data, "r")

    if not check_safe_archive(destination_path, archive):
        raise ValueError("Unsafe archive; contains unexpected file paths. Plugin may be malicious.")

    for name in archive.getnames():
        destination_file_path = Path.resolve(destination_path / name)
        with open(destination_file_path, "b") as f:
            f.write(archive.extractfile(name).read())


class PluginRegistry:
    def __init__(
        self, island_api_client: IIslandAPIClient, plugin_loader: PluginLoader, plugin_dir: Path
    ):
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
        self._plugin_dir = plugin_dir

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: AgentPluginType) -> None:
        self._registry.setdefault(plugin_type, {})
        self._registry[plugin_type][plugin_name] = plugin

        logger.debug(f"Plugin '{plugin_name}' loaded")

    def get_plugin(self, plugin_name: str, plugin_type: AgentPluginType) -> Any:
        try:
            plugin = self._registry[plugin_type][plugin_name]
        except KeyError:
            try:
                agent_plugin = self._island_api_client.get_agent_plugin(plugin_type, plugin_name)
                plugin_folder_name = f"{plugin_name}-{plugin_type.value.lower()}"
                plugin_dir = self._plugin_dir / plugin_folder_name
                extract_plugin(agent_plugin.source_archive, plugin_dir)
                multiprocessing_plugin = self._plugin_loader.load_multiprocessing_plugin(
                    plugin_name=plugin_folder_name, main_thread_name=current_thread().name
                )
                plugin = copy(multiprocessing_plugin)
            except IslandAPIRequestError:
                raise UnknownPluginError(
                    f"Unknown plugin '{plugin_name}' of type '{plugin_type.value}'"
                )
            except ValueError as err:
                raise ValueError(
                    f"Unsafe plugin '{plugin_name}' of type '{plugin_type.value}'", err
                )
            except Exception as err:
                raise Exception(
                    f"Unexpected response received while fetching "
                    f"plugin '{plugin_name}' of type '{plugin_type.value}' from Island",
                    err,
                )

        logger.debug(f"Plugin '{plugin_name}' found")

        return plugin
