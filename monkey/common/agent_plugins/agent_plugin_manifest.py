import re
from typing import Optional, Tuple

from pydantic import validator

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from common.base_models import InfectionMonkeyBaseModel


class AgentPluginManifest(InfectionMonkeyBaseModel):
    """
    Class describing agent plugin

    Attributes:
        :param name: Plugin name in snake case
        :param plugin_type: Type of the plugin (exploiter, fingerprinter,
         credential collector, etc.)
        :param supported_operating_systems: List of operating systems the plugin supports
        :param title: Human readable name for the plugin
        :param description: Description of the plugin
        :param link_to_documentation: Link to the documentation of the plugin
        :param safe: Is the plugin safe to run. If there's a chance that running the plugin could
         disrupt the regular activities of the servers or the network, then the plugin is not safe.
    """

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

    @validator("name")
    def validate_name(cls, name):
        valid_name_regex = re.compile("^[a-zA-Z0-9_-]+$")
        if not re.match(valid_name_regex, name):
            raise ValueError(f"Agent plugin name contains invalid characters: {name}")

        return name
