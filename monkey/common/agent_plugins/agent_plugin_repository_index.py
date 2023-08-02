import time
from typing import Dict, List, Literal, Union

from pydantic import Field
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
