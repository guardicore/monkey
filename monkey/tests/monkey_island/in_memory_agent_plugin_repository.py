from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository


class InMemoryAgentPluginRepository(IAgentPluginRepository):
    def __init__(self):
        self._plugins = {}

    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        return self._plugins[name]

    def save_plugin(self, name: str, plugin: AgentPlugin):
        self._plugins[name] = plugin
