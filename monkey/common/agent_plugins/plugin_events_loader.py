import importlib
import sys
from pathlib import Path
from typing import Iterable, Type

from typing_extensions import Protocol

from common.agent_event_serializers import IAgentEventSerializerRegistry
from common.agent_events import AgentEventRegistry


class PluginEvents(Protocol):
    def get_event_classes(self) -> Iterable[Type]:
        pass

    def register_event_serializers(self, registry: IAgentEventSerializerRegistry):
        pass

    def register_events(self, registry: AgentEventRegistry):
        pass


def load_events(plugin_name: str, plugin_path: Path) -> PluginEvents:
    """
    Load the events from the plugin
    """

    # Add plugin path to sys.path
    # TODO: Prepend instead?
    sys.path.append(str(plugin_path))

    # Import API
    plugin_class = importlib.import_module(f"{plugin_name}.events").Events
    return plugin_class()
