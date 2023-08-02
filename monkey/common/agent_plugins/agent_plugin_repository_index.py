import time
from typing import Dict, List, Literal, Union

from pydantic import Field, validator
from semver import VersionInfo

from common.base_models import InfectionMonkeyBaseModel

from . import AgentPluginMetadata, AgentPluginType


class AgentPluginRepositoryIndex(InfectionMonkeyBaseModel):
    """
    Class for an Agent plugin repository's index

    Attributes:
        :param timestamp: The time at which the repository was
                          last updated (seconds since the Unix epoch)
        :param compatible_infection_monkey_version: Version of Infection Monkey that is
                                                    compatible with the plugins in the repository
        :param plugins: Plugins' metadata, segregated by type and sorted by version
    """

    timestamp: float = Field(default_factory=time.time)
    compatible_infection_monkey_version: Union[VersionInfo, Literal["development"]]
    plugins: Dict[AgentPluginType, Dict[str, List[AgentPluginMetadata]]]

    @validator("plugins")
    def sort_plugins_by_version(cls, plugins):
        # if a plugin has multiple versions, this sorts them in ascending order
        for plugin_type in plugins:
            for plugin_name in plugins[plugin_type]:
                plugin_versions = plugins[plugin_type][plugin_name]
                plugin_versions.sort(lambda plugin_version: plugin_version.version)

        return plugins
