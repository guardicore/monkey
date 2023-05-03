from abc import ABC, abstractmethod

from monkey_island.cc.models import AgentID


class IAgentLogRepository(ABC):
    """A repository used to store `Agent` logs"""

    @abstractmethod
    def upsert_agent_log(self, agent_id: AgentID, log_contents: str):
        """
        Upsert (insert or update) the log contents for a particular agent


        :param agent_id: The ID of the `Agent` that generated the log
        :param log_contents: The log contents
        :raises StorageError: If an error occurs while attempting to store the log
        """

    @abstractmethod
    def get_agent_log(self, agent_id: AgentID) -> str:
        """
        Get the log for a specific agent

        :param agent_id: The ID of the `Agent` that generated the log
        :return: The log contents for the requested `Agent`
        :raises UnknownRecordError: If no log for the requested `Agent` is available
        :raises RetrievalError: If an error occurs while attempting to retrieve the log
        """

    @abstractmethod
    def reset(self):
        """
        Removes all data from the repository

        :raises RemovalError: If an error occurs while attempting to reset the repository
        """
