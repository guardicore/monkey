from common.agent_events import OSDiscoveryEvent
from monkey_island.cc.repository import IAgentRepository, IMachineRepository


class update_machine_os:
    def __init__(self, agent_repository: IAgentRepository, machine_repository: IMachineRepository):
        self._agent_repository = agent_repository
        self._machine_repository = machine_repository

    def __call__(self, event: OSDiscoveryEvent):
        # Get the agent machine
        agent = self._agent_repository.get_agent_by_id(event.source)
        machine = self._machine_repository.get_machine_by_id(agent.machine_id)

        # Update the machine
        machine.operating_system = event.os
        machine.operating_system_version = event.version
        self._machine_repository.upsert_machine(machine)
