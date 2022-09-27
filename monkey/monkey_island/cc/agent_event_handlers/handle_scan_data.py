from ipaddress import IPv4Address
from logging import getLogger

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


class handle_scan_data:
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
        try:
            # Get or create the destination machine
            # NOTE: Assuming IP's are unique for now
            if not isinstance(event.target, IPv4Address):
                logger.error("Unable to process scan data: Unknown target")
                return
            dest_machines = self._machine_repository.get_machines_by_ip(event.target)
            if not dest_machines:
                machine = Machine(id=self._machine_repository.get_new_id())
                dest_machines = [machine]
                self._machine_repository.upsert_machine(machine)

            # Update the destination machine
            dest_machine = dest_machines[0]
            if event.scan_data.os is not None:
                dest_machine.operating_system = event.scan_data.os
                self._machine_repository.upsert_machine(dest_machine)

            # Get the source machine
            agent = self._agent_repository.get_agent_by_id(event.source)
            src_machine = self._machine_repository.get_machine_by_id(agent.machine_id)

            # Update or create the node
            self._node_repository.upsert_communication(
                src_machine.id, dest_machine.id, CommunicationType.SCANNED
            )
        except (RetrievalError, StorageError, UnknownRecordError) as err:
            logger.error(f"Unable to process scan data: {err}")
