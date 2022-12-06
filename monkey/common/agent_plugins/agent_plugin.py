from base64 import b64encode
from typing import Any, Dict

from common.agent_plugins import AgentPluginManifest
from common.base_models import InfectionMonkeyBaseModel
from common.types.b64_bytes import B64Bytes


class AgentPlugin(InfectionMonkeyBaseModel):
    """
    Class describing agent plugin

    Attributes:
        :param plugin_manifest: Metadata describing the plugin
        :param config_schema: JSONSchema describing the configuration options
        :param default_config: Dictionary of default configuration options
        :param source_archive: Contents of the plugin codebase
    """

    plugin_manifest: AgentPluginManifest
    # Should be JSONSerializable but it's only supported in 3.9:
    # https://github.com/pydantic/pydantic/pull/1844
    config_schema: Dict[str, Any]
    default_config: Dict[str, Any]
    source_archive: B64Bytes

    class Config:
        json_encoders = {bytes: lambda byte_field: b64encode(byte_field).decode()}
