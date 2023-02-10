from abc import ABC, abstractmethod
from typing import Sequence

from monkey_island.cc.models import Agent, AgentID


class IAgentRepository(ABC):
    """A repository used to store and retrieve `Agent` objects"""

    @abstractmethod
    def upsert_agent(self, agent: Agent):
        """
        Upsert (insert or update) an `Agent`

        Insert the `Agent` if no `Agent` with a matching ID exists in the repository. If the agent
        already exists, update it.

        :param agent: The `agent` to be inserted or updated
        :raises StorageError: If an error occurs while attempting to store the `Agent`
        """

    @abstractmethod
    def get_agents(self) -> Sequence[Agent]:
        """
        Get all `Agents` stored in the repository

        :return: All agents in the repository
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Agents`
        """

    @abstractmethod
    def get_agent_by_id(self, agent_id: AgentID) -> Agent:
        """
        Get an `Agent` by ID

        :param agent_id: The ID of the `Agent` to be retrieved
        :return: An `Agent` with a matching `id`
        :raises UnknownRecordError: If an `Agent` with the specified `id` does not exist in the
                                    repository
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Agent`
        """

    @abstractmethod
    def get_running_agents(self) -> Sequence[Agent]:
        """
        Get all `Agents` that are currently running

        :return: All `Agents` that are currently running
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Agents`
        """

    @abstractmethod
    def get_progenitor(self, agent: Agent) -> Agent:
        """
        Gets the progenitor `Agent` for the agent.

        :param agent: The Agent for which we want the progenitor
        :return: `Agent` progenitor ( an initial agent that started the exploitation chain)
        :raises RetrievalError: If an error occurrs while attempting to retrieve the `Agent`
        :raises UnknownRecordError: If the agent ID is not in the repository
        """

    @abstractmethod
    def reset(self):
        """
        Removes all data from the repository
        """
