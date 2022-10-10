from functools import lru_cache
from ipaddress import IPv4Address, IPv4Interface

from common.agent_events import AbstractAgentEvent
from common.types import AgentID, MachineID
from monkey_island.cc.models import CommunicationType, Machine
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    UnknownRecordError,
)


class NodeUpdateFacade:
    def __init__(
        self,
        agent_repository: IAgentRepository,
        machine_repository: IMachineRepository,
        node_repository: INodeRepository,
    ):
        self._agent_repository = agent_repository
        self._machine_repository = machine_repository
        self._node_repository = node_repository

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
        machine_id = self.get_machine_id_from_agent_id(event.source)
        return self._machine_repository.get_machine_by_id(machine_id)

    @lru_cache(maxsize=None)
    def get_machine_id_from_agent_id(self, agent_id: AgentID) -> MachineID:
        return self._agent_repository.get_agent_by_id(agent_id).machine_id

    def upsert_communication_from_event(
        self, event: AbstractAgentEvent, communication_type: CommunicationType
    ):
        if not isinstance(event.target, IPv4Address):
            raise TypeError("Event targets must be of type IPv4Address")

        source_machine_id = self.get_machine_id_from_agent_id(event.source)
        target_machine = self.get_or_create_target_machine(event.target)

        self._node_repository.upsert_communication(
            source_machine_id, target_machine.id, communication_type
        )
