from typing import Optional, Tuple

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from common.base_models import InfectionMonkeyBaseModel


class AgentPluginManifest(InfectionMonkeyBaseModel):
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
