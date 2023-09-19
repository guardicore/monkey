import time
from typing import Any, Dict, List, Literal, Union

from pydantic import Field, validator
from semver import VersionInfo

from common.base_models import MutableInfectionMonkeyBaseModel, MutableInfectionMonkeyModelConfig

from . import AgentPluginMetadata, AgentPluginType, PluginName

DEVELOPMENT = "development"


class AgentPluginRepositoryIndex(MutableInfectionMonkeyBaseModel):
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
        VersionInfo, Literal[f"{DEVELOPMENT}"]
    ]
    plugins: Dict[AgentPluginType, Dict[PluginName, List[AgentPluginMetadata]]]

    class Config(MutableInfectionMonkeyModelConfig):
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            **AgentPluginMetadata.Config.json_encoders,
            VersionInfo: lambda v: str(v),
        }

    @validator("plugins")
    def _sort_plugins_by_version(cls, plugins):
        # if a plugin has multiple versions, this sorts them in ascending order
        for plugin_type in plugins:
            for plugin_name in plugins[plugin_type]:
                plugin_versions = plugins[plugin_type][plugin_name]
                plugin_versions.sort(key=lambda plugin_version: plugin_version.version)

        return plugins

    @validator("compatible_infection_monkey_version", pre=True)
    def _infection_monkey_version_parser(
        cls, value: Union[VersionInfo, str, Dict[str, Any]]
    ) -> Union[VersionInfo, Literal[f"{DEVELOPMENT}"]]:  # type: ignore[valid-type]
        if isinstance(value, VersionInfo):
            return value

        if isinstance(value, str):
            if value == DEVELOPMENT:
                return value

            return VersionInfo.parse(value)

        raise TypeError(f'Expected "{DEVELOPMENT}" or a valid semantic version, got {type(value)}')

    @validator("plugins")
    def _convert_str_type_to_enum(cls, plugins):
        return {AgentPluginType(t): plugins for t, plugins in plugins.items()}
