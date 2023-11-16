from monkeyevents import HostnameDiscoveryEvent

from monkey_island.cc.repositories import AgentMachineFacade


class update_machine_hostname:
    def __init__(self, agent_machine_facade: AgentMachineFacade):
        self._agent_machine_facade = agent_machine_facade

    def __call__(self, event: HostnameDiscoveryEvent):
        machine = self._agent_machine_facade.get_agent_machine(event.source)
        machine.hostname = event.hostname
        self._agent_machine_facade.upsert_machine(machine)
