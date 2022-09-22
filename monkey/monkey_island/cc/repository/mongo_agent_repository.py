from typing import Sequence

from pymongo import MongoClient

from monkey_island.cc.models import Agent, AgentID
from monkey_island.cc.repository import (
    IAgentRepository,
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

from .consts import MONGO_OBJECT_ID_KEY


class MongoAgentRepository(IAgentRepository):
    def __init__(self, mongo_client: MongoClient):
        self._agents_collection = mongo_client.monkey_island.agents

    def upsert_agent(self, agent: Agent):
        try:
            result = self._agents_collection.replace_one(
                {"id": str(agent.id)}, agent.dict(simplify=True), upsert=True
            )
        except Exception as err:
            raise StorageError(f'Error updating agent with ID "{agent.id}": {err}')

        if result.matched_count != 0 and result.modified_count != 1:
            raise StorageError(
                f'Error updating agent with ID "{agent.id}": Expected to update 1 agent, '
                f"but {result.modified_count} were updated"
            )

        if result.matched_count == 0 and result.upserted_id is None:
            raise StorageError(
                f'Error inserting agent with ID "{agent.id}": Expected to insert 1 agent, '
                f"but no agents were inserted"
            )

    def get_agent_by_id(self, agent_id: AgentID) -> Agent:
        try:
            agent_dict = self._agents_collection.find_one(
                {"id": str(agent_id)}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise RetrievalError(f'Error retrieving agent with "id == {agent_id}": {err}')

        if agent_dict is None:
            raise UnknownRecordError(f'Unknown ID "{agent_id}"')

        return Agent(**agent_dict)

    def get_running_agents(self) -> Sequence[Agent]:
        try:
            cursor = self._agents_collection.find({"stop_time": None}, {MONGO_OBJECT_ID_KEY: False})
            return list(map(lambda a: Agent(**a), cursor))
        except Exception as err:
            raise RetrievalError(f"Error retrieving running agents: {err}")

    def get_progenitor(self, agent: Agent) -> Agent:
        if agent.parent_id is None:
            return agent

        parent = self.get_agent_by_id(agent.parent_id)

        return self.get_progenitor(parent)

    def reset(self):
        try:
            self._agents_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")
