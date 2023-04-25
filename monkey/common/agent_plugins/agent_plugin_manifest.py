from typing import Callable, Mapping, Optional, Tuple, Type

from pydantic import HttpUrl

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from common.base_models import InfectionMonkeyBaseModel, InfectionMonkeyModelConfig
from common.types import PluginName, PluginVersion


class AgentPluginManifest(InfectionMonkeyBaseModel):
    """
    Class describing agent plugin

    Attributes:
        :param name: Plugin name in snake case
        :param plugin_type: Type of the plugin (exploiter, fingerprinter,
         credentials collector, etc.)
        :param supported_operating_systems: Operating systems that the plugin can run on
        :param target_operating_systems: Operating systems that the plugin can target
        :param title: Human readable name for the plugin
        :param description: Description of the plugin
        :param version: Version of the plugin
        :param link_to_documentation: Link to the documentation of the plugin
        :param safe: Is the plugin safe to run. If there's a chance that running the plugin could
         disrupt the regular activities of the servers or the network, then the plugin is not safe.
    """

    name: PluginName
    plugin_type: AgentPluginType
    supported_operating_systems: Tuple[OperatingSystem, ...] = (
        OperatingSystem.WINDOWS,
        OperatingSystem.LINUX,
    )
    target_operating_systems: Tuple[OperatingSystem, ...] = (
        OperatingSystem.WINDOWS,
        OperatingSystem.LINUX,
    )
    title: Optional[str]
    version: PluginVersion
    description: Optional[str]
    remediation_suggestion: Optional[str]
    link_to_documentation: Optional[HttpUrl]
    safe: bool = False

    class Config(InfectionMonkeyModelConfig):
        json_encoders: Mapping[Type, Callable] = {PluginVersion: lambda v: str(v)}
