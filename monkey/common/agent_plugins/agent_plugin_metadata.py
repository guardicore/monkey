from pathlib import PurePosixPath
from typing import Any, Union

from monkeytypes import AgentPluginType, InfectionMonkeyBaseModel
from pydantic import ConfigDict, Field, field_serializer, field_validator

from . import PluginName, PluginVersion


class AgentPluginMetadata(InfectionMonkeyBaseModel):
    """
    Class for an Agent plugin's metadata

    Attributes:
        :param name: Plugin name
        :param plugin_type: Plugin type
        :param resource_path: Path of the plugin package within the repository
        :param sha256: Plugin file checksum
        :param description: Plugin description
        :param version: Plugin version
        :param safe: Whether the plugin is safe for use in production environments
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: PluginName
    plugin_type: AgentPluginType
    resource_path: PurePosixPath
    sha256: str = Field(pattern=r"^[0-9a-fA-F]{64}$")
    description: str
    version: PluginVersion
    safe: bool

    @field_serializer("resource_path", "version", when_used="json")
    def dump_string(self, v: Any):
        return str(v)

    @field_validator("resource_path", mode="before")
    @classmethod
    def _str_to_pure_posix_path(cls, value: Union[PurePosixPath, str]) -> PurePosixPath:
        if isinstance(value, PurePosixPath):
            return value

        if isinstance(value, str):
            return PurePosixPath(value)

        raise TypeError(f"Expected PurePosixPath or str but got {type(value)}")
