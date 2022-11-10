from functools import lru_cache

from common.types import AgentID, MachineID
from monkey_island.cc.models import Machine
from monkey_island.cc.repository import IAgentRepository, IMachineRepository


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

    def update_agent_machine(self, agent_id: AgentID, machine: Machine):
        """
        Update the machine for a given Agent

        :param agent_id: The AgentID of the Agent
        :param machine: The updated Machine
        :raises UnknownRecordError: If no `Machine` for the specified `agent_id` could be found
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Machine`
        :raises ValueError: If `machine`'s ID does not match the Agent's machine ID
        :raises StorageError: If a problem occurred while attempting to store the `Machine`
        """
        machine_id = self.get_machine_id_from_agent_id(agent_id)
        if machine.id != machine_id:
            raise ValueError("Machine's ID does not match the agent's machine ID")

        self._machine_repository.upsert_machine(machine)

    def reset_cache(self):
        self.get_machine_id_from_agent_id.cache_clear()
