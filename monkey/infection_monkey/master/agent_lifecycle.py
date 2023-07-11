from infection_monkey.island_api_client import IIslandAPIClient


class AgentLifecycle:
    def __init__(self, island_api_client: IIslandAPIClient):
        self._island_api_client = island_api_client

    def should_agent_stop(self) -> bool:
        agent_signals = self._island_api_client.get_agent_signals()
        return agent_signals.terminate is not None
