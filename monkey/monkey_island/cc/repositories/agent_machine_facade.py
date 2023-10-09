from functools import lru_cache

from monkeytypes import AgentID, MachineID

from monkey_island.cc.models import Machine
from monkey_island.cc.repositories import IAgentRepository, IMachineRepository


class AgentMachineFacade:
    """
    A simple facade for getting the Machine for an Agent
    """

    def __init__(self, agent_repository: IAgentRepository, machine_repository: IMachineRepository):
        self._agent_repository = agent_repository
        self._machine_repository = machine_repository

    @lru_cache(maxsize=8192)
    def get_machine_id_from_agent_id(self, agent_id: AgentID) -> MachineID:
        """
        Given an AgentID, get the MachineID of the machine the Agent ran on

        :param agent_id: An AgentID
        :return: The MachineID of the Machine that the Agent ran on
        :raises UnknownRecordError: If no `Agent` with the specified `agent_id` could be found
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Agent`
        """
        return self._agent_repository.get_agent_by_id(agent_id).machine_id

    def get_agent_machine(self, agent_id: AgentID) -> Machine:
        """
        Get the Machine for a given Agent, by AgentID

        :param agent_id: AgentID of the Agent
        :return: Machine that the Agent ran on
        :raises UnknownRecordError: If no `Machine` for the specified `agent_id` could be found
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Machine`
        """
        machine_id = self.get_machine_id_from_agent_id(agent_id)
        return self._machine_repository.get_machine_by_id(machine_id)

    def upsert_machine(self, machine: Machine):
        """
        Upsert (insert or update) a `Machine`

        See :meth:`monkey_island.cc.models.Machine.upsert_machine`
        """
        self._machine_repository.upsert_machine(machine)

    def reset_cache(self):
        self.get_machine_id_from_agent_id.cache_clear()
