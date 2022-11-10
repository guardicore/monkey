from common.agent_events import OSDiscoveryEvent
from monkey_island.cc.repository import AgentMachineFacade, IMachineRepository


class update_machine_os:
    def __init__(
        self, agent_machine_facade: AgentMachineFacade, machine_repository: IMachineRepository
    ):
        self._agent_machine_facade = agent_machine_facade
        self._machine_repository = machine_repository

    def __call__(self, event: OSDiscoveryEvent):
        # Get the agent machine
        machine = self._agent_machine_facade.get_agent_machine(event.source)

        # Update the machine
        machine.operating_system = event.os
        machine.operating_system_version = event.version
        self._machine_repository.upsert_machine(machine)
