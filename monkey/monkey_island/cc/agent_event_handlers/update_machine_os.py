from monkeyevents import OSDiscoveryEvent

from monkey_island.cc.repositories import AgentMachineFacade


class update_machine_os:
    def __init__(self, agent_machine_facade: AgentMachineFacade):
        self._agent_machine_facade = agent_machine_facade

    def __call__(self, event: OSDiscoveryEvent):
        # Get the agent machine
        machine = self._agent_machine_facade.get_agent_machine(event.source)

        # Update the machine
        machine.operating_system = event.os
        machine.operating_system_version = event.version
        self._agent_machine_facade.upsert_machine(machine)
