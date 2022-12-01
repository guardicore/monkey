from typing import Optional, Tuple

from common import OperatingSystem

from .agent_plugin_type import AgentPluginType


class AgentPluginManifest:
    name: str
    plugin_type: AgentPluginType
    supported_operating_systems: Tuple[OperatingSystem, ...] = (
        OperatingSystem.WINDOWS,
        OperatingSystem.LINUX,
    )
    title: Optional[str]
    description: Optional[str]
    link_to_documentation: Optional[str]
    safe: bool = False
