from pathlib import PurePosixPath

from pydantic import Field
from semver import VersionInfo

from common.base_models import InfectionMonkeyBaseModel

from . import AgentPluginType


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

    name: str
    type_: AgentPluginType
    resource_path: PurePosixPath
    sha256: str = Field(regex=r"^[0-9a-fA-F]{64}$")
    description: str
    version: VersionInfo
    safe: bool

    class Config:
        arbitrary_types_allowed = True
