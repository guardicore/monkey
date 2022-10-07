from functools import lru_cache
from ipaddress import IPv4Address, IPv4Interface

from common.agent_events import AbstractAgentEvent
from common.types import AgentID, MachineID
from monkey_island.cc.models import Machine
from monkey_island.cc.repository import IAgentRepository, IMachineRepository, UnknownRecordError


class NodeUpdateFacade:
    def __init__(self, agent_repository: IAgentRepository, machine_repository: IMachineRepository):
        self._agent_repository = agent_repository
        self._machine_repository = machine_repository

    def get_or_create_target_machine(self, target: IPv4Address):
        try:
            target_machines = self._machine_repository.get_machines_by_ip(target)
            return target_machines[0]
        except UnknownRecordError:
            machine = Machine(
                id=self._machine_repository.get_new_id(),
                network_interfaces=[IPv4Interface(target)],
            )
            self._machine_repository.upsert_machine(machine)
            return machine

    def get_event_source_machine(self, event: AbstractAgentEvent) -> Machine:
        machine_id = self._get_machine_id_from_agent_id(event.source)
        return self._machine_repository.get_machine_by_id(machine_id)

    @lru_cache(maxsize=None)
    def _get_machine_id_from_agent_id(self, agent_id: AgentID) -> MachineID:
        return self._agent_repository.get_agent_by_id(agent_id).machine_id
