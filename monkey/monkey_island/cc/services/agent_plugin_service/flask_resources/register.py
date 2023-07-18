from monkey_island.cc.flask_utils import FlaskDIWrapper

from .agent_plugins import AgentPlugins
from .agent_plugins_manifest import AgentPluginsManifest


def register_resources(api: FlaskDIWrapper):
    api.add_resource(AgentPlugins)
    api.add_resource(AgentPluginsManifest)
