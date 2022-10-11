from typing import Sequence

from common.types import AgentID
from monkey_island.cc.models import Agent
from monkey_island.cc.repository import IAgentRepository, UnknownRecordError


class InMemoryAgentRepository(IAgentRepository):
    def __init__(self):
        self._agents = []

    def upsert_agent(self, agent: Agent):
        for position, existing_agent in enumerate(self._agents):
            if existing_agent.id == agent:
                self._agents[position] = agent
                return
        self._agents.append(agent)

    def get_agents(self) -> Sequence[Agent]:
        return self._agents

    def get_agent_by_id(self, agent_id: AgentID) -> Agent:
        for agent in self._agents:
            if agent.id == agent_id:
                return agent
        raise UnknownRecordError(f'Unknown ID "{agent_id}"')

    def get_running_agents(self):
        raise NotImplementedError

    def get_progenitor(self, _):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
