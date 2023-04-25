from common.agent_plugins import AgentPluginManifest, AgentPluginType
from common.operating_system import OperatingSystem

HARD_CODED_CREDENTIALS_COLLECTOR_MANIFESTS = {
    "MimikatzCollector": AgentPluginManifest(
        name="MimikatzCollector",
        plugin_type=AgentPluginType.CREDENTIAL_COLLECTOR,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.WINDOWS,),
        title="Mimikatz Credentials Collector",
        version="1.0.0",
        description="Collects credentials from Windows credential manager.",
        safe=True,
    ),
    "SSHCollector": AgentPluginManifest(
        name="SSHCollector",
        plugin_type=AgentPluginType.CREDENTIAL_COLLECTOR,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX,),
        title="SSH Credentials Collector",
        version="1.0.0",
        description="Searches users' home directories and collects SSH keypairs.",
        safe=True,
    ),
}
