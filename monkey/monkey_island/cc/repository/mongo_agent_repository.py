from typing import Any, MutableMapping, Sequence

from pymongo import MongoClient

from monkey_island.cc.models import Agent, AgentID
from monkey_island.cc.repository import (
    IAgentRepository,
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
            agent_dict = self._agents_collection.find_one({"id": str(agent_id)})
        except Exception as err:
            raise RetrievalError(f'Error retrieving agent with "id == {agent_id}": {err}')

        if agent_dict is None:
            raise UnknownRecordError(f'Unknown ID "{agent_id}"')

        return MongoAgentRepository._mongo_record_to_agent(agent_dict)

    def get_running_agents(self) -> Sequence[Agent]:
        try:
            cursor = self._agents_collection.find({"stop_time": None})
            return list(map(MongoAgentRepository._mongo_record_to_agent, cursor))
        except Exception as err:
            raise RetrievalError(f"Error retrieving running agents: {err}")

    @staticmethod
    def _mongo_record_to_agent(mongo_record: MutableMapping[str, Any]) -> Agent:
        del mongo_record[MONGO_OBJECT_ID_KEY]
        return Agent(**mongo_record)

    def reset(self):
        pass
