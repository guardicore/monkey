from monkey_island.cc.flask_utils import FlaskDIWrapper

from .agent_plugins import AgentPlugins
from .agent_plugins_manifest import AgentPluginsManifest
from .install_agent_plugin import InstallAgentPlugin
from .installed_agent_plugins_manifests import InstalledAgentPluginsManifests


def register_resources(api: FlaskDIWrapper):
    api.add_resource(AgentPlugins)
    api.add_resource(AgentPluginsManifest)
    api.add_resource(InstallAgentPlugin)
    api.add_resource(InstalledAgentPluginsManifests)
