import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Iterable, List, Type

from typing_extensions import Protocol

from common.agent_event_serializers import IAgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent


class PluginEvents(Protocol):
    def register_event_serializers(self, registry: IAgentEventSerializerRegistry):
        pass


def get_plugin_event_classes(
    plugin_name: str, plugin_path: Path, event_names: Iterable[str]
) -> Iterable[Type[AbstractAgentEvent]]:
    """
    Load the events from the plugin

    :param plugin_name: The name of the plugin to load
    :param plugin_path: The path of the plugins folder
    :param event_names: The names of the events to load
    :return: The event types
    """

    # Import API
    events: List[Type[AbstractAgentEvent]] = []
    events_module = _get_events_module(plugin_name, plugin_path)
    for event_name in event_names:
        event_type = getattr(events_module, event_name)
        events.append(event_type)

    return events


def _get_events_module(plugin_name: str, plugin_path: Path) -> ModuleType:
    return sys.modules.get(f"{plugin_name}.events") or _import_events_module(
        plugin_name, plugin_path
    )


def _import_events_module(plugin_name: str, plugin_path: Path) -> ModuleType:
    # Add plugin path to sys.path
    plugin_path_str = str(plugin_path)
    if plugin_path_str not in sys.path:
        sys.path.append(plugin_path_str)

    return importlib.import_module(f"{plugin_name}.events")


def load_events(plugin_name: str, plugin_path: Path) -> PluginEvents:
    """
    Load the events from the plugin

    :param plugin_name: The name of the plugin to load
    :param plugin_path: The path of the plugins folder
    :return: The plugin events
    """

    # Import API
    events_module = _get_events_module(plugin_name, plugin_path)

    plugin_class = events_module.Events
    return plugin_class()
