from common.agent_plugins import AgentPluginManifest, AgentPluginType
from common.operating_system import OperatingSystem

HARD_CODED_CREDENTIALS_COLLECTOR_MANIFESTS = {
    "SSHCollector": AgentPluginManifest(
        name="SSHCollector",
        plugin_type=AgentPluginType.CREDENTIALS_COLLECTOR,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX,),
        title="SSH Credentials Collector",
        version="1.0.0",
        description="Searches users' home directories and collects SSH keypairs.",
        safe=True,
    ),
}
