import copy
from typing import Sequence

from monkeytypes import AgentID

from monkey_island.cc.models import Agent
from monkey_island.cc.repositories import IAgentRepository, UnknownRecordError


class InMemoryAgentRepository(IAgentRepository):
    def __init__(self):
        self._agents = {}

    def upsert_agent(self, agent: Agent):
        self._agents[agent.id] = copy.deepcopy(agent)

    def get_agents(self) -> Sequence[Agent]:
        return list(self._agents.values())

    def get_agent_by_id(self, agent_id: AgentID) -> Agent:
        try:
            return self._agents[agent_id]
        except KeyError:
            raise UnknownRecordError(f'Unknown ID "{agent_id}"')

    def get_running_agents(self) -> Sequence[Agent]:
        return [agent for agent in self._agents.values() if agent.stop_time is None]

    def get_progenitor(self, _: Agent) -> Agent:
        raise NotImplementedError

    def reset(self):
        self._agents = {}
