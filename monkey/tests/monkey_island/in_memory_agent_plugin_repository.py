from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository, UnknownRecordError


class InMemoryAgentPluginRepository(IAgentPluginRepository):
    def __init__(self):
        self._plugins = {}

    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        if name not in self._plugins:
            raise UnknownRecordError(f"Plugin '{name}' does not exist.")
        return self._plugins[name]

    def save_plugin(self, name: str, plugin: AgentPlugin):
        self._plugins[name] = plugin
