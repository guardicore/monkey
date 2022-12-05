from common.agent_plugins import AgentPluginManifest
from common.base_models import InfectionMonkeyBaseModel
from common.types import JSONSerializable


class AgentPlugin(InfectionMonkeyBaseModel):
    plugin_manifest: AgentPluginManifest
    config_schema: JSONSerializable
    default_config: JSONSerializable
    source_archive: bytes
