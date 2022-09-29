from logging import getLogger

from pydantic.json import IPv4Interface

from common.agent_events import PingScanEvent
from monkey_island.cc.models import CommunicationType, Machine
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

logger = getLogger(__name__)


class handle_ping_scan_event:
    """
    Handles ping scan event and makes changes to Machine and Node states based on it
    :param event: Ping scan event
    """

    def __init__(
        self,
        agent_repository: IAgentRepository,
        machine_repository: IMachineRepository,
        node_repository: INodeRepository,
    ):
        self._agent_repository = agent_repository
        self._machine_repository = machine_repository
        self._node_repository = node_repository

    def __call__(self, event: PingScanEvent):
        if not event.response_received:
            return

        try:
            target_machine = self._get_target_machine(event)

            self._update_target_machine_os(target_machine, event)
            self._update_nodes(target_machine, event)
        except (RetrievalError, StorageError, TypeError, UnknownRecordError):
            logger.exception("Unable to process ping scan data")

    def _get_target_machine(self, event: PingScanEvent) -> Machine:
        try:
            target_machines = self._machine_repository.get_machines_by_ip(event.target)
            return target_machines[0]
        except UnknownRecordError:
            machine = Machine(
                id=self._machine_repository.get_new_id(),
                network_interfaces=[IPv4Interface(event.target)],
            )
            self._machine_repository.upsert_machine(machine)
            return machine

    def _update_target_machine_os(self, machine: Machine, event: PingScanEvent):
        if event.os is not None and machine.operating_system is None:
            machine.operating_system = event.os
            self._machine_repository.upsert_machine(machine)

    def _update_nodes(self, target_machine, event):
        src_machine = self._get_source_machine(event)

        # Update or create the node
        self._node_repository.upsert_communication(
            src_machine.id, target_machine.id, CommunicationType.SCANNED
        )

    def _get_source_machine(self, event: PingScanEvent) -> Machine:
        agent = self._agent_repository.get_agent_by_id(event.source)
        return self._machine_repository.get_machine_by_id(agent.machine_id)
