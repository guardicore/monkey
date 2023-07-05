from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, AgentPluginType

EXPLOITER_NAME_1 = "MockExploiter"
EXPLOITER_NAME_2 = "MockExploiter2"
EXPLOITER_INCOMPLETE_MANIFEST = "MockExploiter3"
EXPLOITER_TITLE_1 = "Mock Exploiter"

REMEDIATION_SUGGESTION_1 = "Fix it!"
REMEDIATION_SUGGESTION_2 = "Patch it!"

PLUGIN_MANIFESTS = {
    AgentPluginType.EXPLOITER: {
        EXPLOITER_NAME_1: AgentPluginManifest(
            name=EXPLOITER_NAME_1,
            plugin_type=AgentPluginType.EXPLOITER,
            title=EXPLOITER_TITLE_1,
            version="1.0.0",
            target_operating_systems=(OperatingSystem.WINDOWS,),
            description="Mocked description",
            link_to_documentation="http://no_mocked.com",
            remediation_suggestion=REMEDIATION_SUGGESTION_1,
            safe=True,
        ),
        EXPLOITER_NAME_2: AgentPluginManifest(
            name=EXPLOITER_NAME_2,
            plugin_type=AgentPluginType.EXPLOITER,
            title=None,
            version="1.0.0",
            target_operating_systems=(OperatingSystem.WINDOWS,),
            description="Another Mocked description",
            link_to_documentation="http://nopenope.com",
            remediation_suggestion=REMEDIATION_SUGGESTION_2,
            safe=True,
        ),
        EXPLOITER_INCOMPLETE_MANIFEST: AgentPluginManifest(
            name=EXPLOITER_INCOMPLETE_MANIFEST,
            plugin_type=AgentPluginType.EXPLOITER,
            target_operating_systems=tuple(),
            version="1.0.0",
        ),
    }
}
