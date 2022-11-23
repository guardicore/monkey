import logging
from typing import Any

from common.types import PluginType
from infection_monkey.i_puppet import UnknownPluginError

logger = logging.getLogger()


class PluginRegistry:
    def __init__(self):
        """
        `self._registry` looks like -
            {
                PluginType.EXPLOITER: {
                    "ZerologonExploiter": ZerologonExploiter,
                    "SMBExploiter": SMBExploiter
                }
            }
        """
        self._registry = {}

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: PluginType) -> None:
        self._registry.setdefault(plugin_type, {})
        self._registry[plugin_type][plugin_name] = plugin

        logger.debug(f"Plugin '{plugin_name}' loaded")

    def get_plugin(self, plugin_name: str, plugin_type: PluginType) -> Any:
        try:
            plugin = self._registry[plugin_type][plugin_name]
        except KeyError:
            raise UnknownPluginError(
                f"Unknown plugin '{plugin_name}' of type '{plugin_type.value}'"
            )

        logger.debug(f"Plugin '{plugin_name}' found")

        return plugin
