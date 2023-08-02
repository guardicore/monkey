from pathlib import PurePosixPath
from typing import Dict, Union

from pydantic import Field, validator
from semver import VersionInfo

from common.base_models import InfectionMonkeyBaseModel

from . import AgentPluginType, PluginName


class AgentPluginMetadata(InfectionMonkeyBaseModel):
    """
    Class for an Agent plugin's metadata

    Attributes:
        :param name: Plugin name
        :param type: Plugin type
        :param resource_path: Path of the plugin file in the AWS S3 bucket
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
    version: VersionInfo
    safe: bool

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PurePosixPath: lambda path: str(path),
            VersionInfo: lambda version: version.to_dict(),
        }

    @validator("resource_path", pre=True)
    def _str_to_pure_posix_path(cls, value: Union[PurePosixPath, str]) -> PurePosixPath:
        if isinstance(value, PurePosixPath):
            return value

        if isinstance(value, str):
            return PurePosixPath(value)

        raise ValueError(f"Expected PurePosixPath or str but got {type(value)}")

    @validator("version", pre=True)
    def _dict_to_version_info(cls, value: Union[VersionInfo, Dict[str, Union[int, None]]]):
        if isinstance(value, VersionInfo):
            return value

        if isinstance(value, dict):
            return VersionInfo(**value)

        raise ValueError(f"Expected VersionInfo or dict but got {type(value)}")
