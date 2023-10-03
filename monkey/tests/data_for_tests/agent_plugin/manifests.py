from monkeytypes import AgentPluginType

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, PluginName

EXPLOITER_NAME_1 = PluginName("MockExploiter")
EXPLOITER_NAME_2 = PluginName("MockExploiter2")
EXPLOITER_INCOMPLETE_MANIFEST = PluginName("MockExploiter3")
EXPLOITER_TITLE_1 = "Mock Exploiter"

CREDENTIALS_COLLECTOR_NAME_1 = PluginName("MockCredentialCollector")

REMEDIATION_SUGGESTION_1 = "Fix it!"
REMEDIATION_SUGGESTION_2 = "Patch it!"

EXPLOITER_MANIFEST_1 = AgentPluginManifest(
    name=EXPLOITER_NAME_1,
    plugin_type=AgentPluginType.EXPLOITER,
    title=EXPLOITER_TITLE_1,
    version="1.0.0",
    target_operating_systems=(OperatingSystem.WINDOWS,),
    description="Mocked description",
    link_to_documentation="http://no_mocked.com",
    remediation_suggestion=REMEDIATION_SUGGESTION_1,
    safe=True,
)

EXPLOITER_MANIFEST_2 = AgentPluginManifest(
    name=EXPLOITER_NAME_2,
    plugin_type=AgentPluginType.EXPLOITER,
    title=None,
    version="1.0.0",
    target_operating_systems=(OperatingSystem.WINDOWS,),
    description="Another Mocked description",
    link_to_documentation="http://nopenope.com",
    remediation_suggestion=REMEDIATION_SUGGESTION_2,
    safe=True,
)

EXPLOITER_MANIFEST_INCOMPLETE = AgentPluginManifest(
    name=EXPLOITER_INCOMPLETE_MANIFEST,
    plugin_type=AgentPluginType.EXPLOITER,
    target_operating_systems=tuple(),
    version="1.0.0",
)

CREDENTIALS_COLLECTOR_MANIFEST_1 = AgentPluginManifest(
    name=CREDENTIALS_COLLECTOR_NAME_1,
    plugin_type=AgentPluginType.CREDENTIALS_COLLECTOR,
    title="Mock Credential Collector",
    version="1.0.0",
    target_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    description="Mocked credential collector",
    link_to_documentation="http://no_mocked.com",
    safe=False,
)

PLUGIN_MANIFESTS = {
    AgentPluginType.EXPLOITER: {
        EXPLOITER_NAME_1: EXPLOITER_MANIFEST_1,
        EXPLOITER_NAME_2: EXPLOITER_MANIFEST_2,
        EXPLOITER_INCOMPLETE_MANIFEST: EXPLOITER_MANIFEST_INCOMPLETE,
    },
    AgentPluginType.CREDENTIALS_COLLECTOR: {
        CREDENTIALS_COLLECTOR_NAME_1: CREDENTIALS_COLLECTOR_MANIFEST_1,
    },
}
