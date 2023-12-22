import time
from typing import Any, Dict, List, Literal, Union

from monkeytypes import AgentPluginType, MutableInfectionMonkeyBaseModel
from pydantic import ConfigDict, Field, field_serializer, field_validator
from semver import VersionInfo

from . import AgentPluginMetadata, PluginName

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

    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)

    timestamp: float = Field(default_factory=time.time)
    # We can't simply use `DEVELOPMENT` here because it throws `pydantic.errors.ConfigError`.
    # This workaround requires us to ignore a mypy error.
    compatible_infection_monkey_version: Union[  # type: ignore[valid-type]
        VersionInfo, Literal[f"{DEVELOPMENT}"]
    ]
    plugins: Dict[AgentPluginType, Dict[PluginName, List[AgentPluginMetadata]]]

    @field_serializer("compatible_infection_monkey_version", when_used="json")
    def dump_compatible_infection_monkey_version(self, v):
        return str(v)

    @field_validator("plugins")
    @classmethod
    def _sort_plugins_by_version(cls, plugins):
        # if a plugin has multiple versions, this sorts them in ascending order
        for plugin_type in plugins:
            for plugin_name in plugins[plugin_type]:
                plugin_versions = plugins[plugin_type][plugin_name]
                plugin_versions.sort(key=lambda plugin_version: plugin_version.version)

        return plugins

    @field_validator("compatible_infection_monkey_version", mode="before")
    @classmethod
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

    @field_validator("plugins")
    @classmethod
    def _convert_str_type_to_enum(cls, plugins):
        return {AgentPluginType(t): plugins for t, plugins in plugins.items()}
