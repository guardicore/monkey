from pathlib import PurePosixPath
from typing import Any, Callable, Dict, Type, Union

from pydantic import Field, validator

from common.base_models import InfectionMonkeyBaseModel, InfectionMonkeyModelConfig

from . import AgentPluginType, PluginName, PluginVersion


class AgentPluginMetadata(InfectionMonkeyBaseModel):
    """
    Class for an Agent plugin's metadata

    Attributes:
        :param name: Plugin name
        :param type: Plugin type
        :param resource_path: Path of the plugin package within the repository
        :param sha256: Plugin file checksum
        :param description: Plugin description
        :param version: Plugin version
        :param safe: Whether the plugin is safe for use in production environments
    """

    name: PluginName
    type_: AgentPluginType
    resource_path: PurePosixPath
    sha256: str = Field(regex=r"^[0-9a-fA-F]{64}$")
    description: str
    version: PluginVersion
    safe: bool

    class Config(InfectionMonkeyModelConfig):
        arbitrary_types_allowed = True
        json_encoders: Dict[Type, Callable[[Any], Any]] = {
            PurePosixPath: lambda path: str(path),
            PluginVersion: lambda v: str(v),
        }

    @validator("resource_path", pre=True)
    def _str_to_pure_posix_path(cls, value: Union[PurePosixPath, str]) -> PurePosixPath:
        if isinstance(value, PurePosixPath):
            return value

        if isinstance(value, str):
            return PurePosixPath(value)

        raise TypeError(f"Expected PurePosixPath or str but got {type(value)}")
