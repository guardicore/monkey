import time
from typing import Any, Dict, List, Literal, Union

from pydantic import Field, validator
from semver import VersionInfo

from common.base_models import InfectionMonkeyBaseModel

from . import AgentPluginMetadata

DEVELOPMENT = "development"


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
    # We can't simply use `DEVELOPMENT` here because it throws `pydantic.errors.ConfigError`.
    # This workaround requires us to ignore a mypy error.
    compatible_infection_monkey_version: Union[  # type: ignore[valid-type]
        VersionInfo, Literal[f"{DEVELOPMENT}"], Dict[str, Any]
    ]
    plugins: Dict[str, Dict[str, List[AgentPluginMetadata]]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            **AgentPluginMetadata.Config.json_encoders,
        }

    @validator("compatible_infection_monkey_version", pre=True)
    def _dict_to_version_info(cls, value: Union[VersionInfo, str, Dict[str, Any]]):
        if (isinstance(value, str) and (value == DEVELOPMENT)) or isinstance(value, VersionInfo):
            return value

        if isinstance(value, dict):
            return VersionInfo(**value)

        raise ValueError(f'Expected "development", VersionInfo, or dict, but got {type(value)}')

    @validator("plugins")
    def _sort_plugins_by_version(cls, plugins):
        # if a plugin has multiple versions, this sorts them in ascending order
        for plugin_type in plugins:
            for plugin_name in plugins[plugin_type]:
                plugin_versions = plugins[plugin_type][plugin_name]
                plugin_versions.sort(key=lambda plugin_version: plugin_version.version)

        return plugins
