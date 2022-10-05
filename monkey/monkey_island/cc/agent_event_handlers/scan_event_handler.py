from logging import getLogger
from typing import List, Union

from typing_extensions import TypeAlias

from common.agent_events import PingScanEvent, TCPScanEvent
from common.types import NetworkPort, NetworkService, PortStatus, SocketAddress
from monkey_island.cc.models import CommunicationType, Machine, Node
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

from .utils import get_or_create_target_machine

ScanEvent: TypeAlias = Union[PingScanEvent, TCPScanEvent]

logger = getLogger(__name__)


class ScanEventHandler:
    """
    Handles scan event and makes changes to Machine and Node states based on it
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

    def handle_ping_scan_event(self, event: PingScanEvent):
        if not event.response_received:
            return

        try:
            target_machine = self._get_target_machine(event)

            self._update_target_machine_os(target_machine, event)
            self._update_nodes(target_machine, event)
        except (RetrievalError, StorageError, UnknownRecordError):
            logger.exception("Unable to process ping scan data")

    def handle_tcp_scan_event(self, event: TCPScanEvent):
        num_open_ports = len(self._get_open_ports(event))

        if num_open_ports <= 0:
            return

        try:
            target_machine = self._get_target_machine(event)
            source_node = self._get_source_node(event)

            self._update_nodes(target_machine, event)
            self._update_tcp_connections(source_node, target_machine, event)
            self._update_network_services(target_machine, event)
        except (RetrievalError, StorageError, UnknownRecordError):
            logger.exception("Unable to process tcp scan data")

    def _get_target_machine(self, event: ScanEvent) -> Machine:
        return get_or_create_target_machine(self._machine_repository, event.target)

    def _get_source_node(self, event: ScanEvent) -> Node:
        machine = self._get_source_machine(event)
        try:
            node = self._node_repository.get_node_by_machine_id(machine.id)
        except UnknownRecordError:
            node = Node(machine_id=machine.id)
            self._node_repository.upsert_node(node)
        return node

    def _get_source_machine(self, event: ScanEvent) -> Machine:
        agent = self._agent_repository.get_agent_by_id(event.source)
        return self._machine_repository.get_machine_by_id(agent.machine_id)

    def _update_target_machine_os(self, machine: Machine, event: PingScanEvent):
        if event.os is not None and machine.operating_system is None:
            machine.operating_system = event.os
            self._machine_repository.upsert_machine(machine)

    def _update_network_services(self, target: Machine, event: TCPScanEvent):
        network_services = {
            SocketAddress(ip=event.target, port=port): NetworkService.UNKNOWN
            for port in self._get_open_ports(event)
        }
        self._machine_repository.upsert_network_services(target.id, network_services)

    @staticmethod
    def _get_open_ports(event: TCPScanEvent) -> List[NetworkPort]:
        return [port for port, status in event.ports.items() if status == PortStatus.OPEN]

    def _update_nodes(self, target_machine: Machine, event: ScanEvent):
        src_machine = self._get_source_machine(event)

        self._node_repository.upsert_communication(
            src_machine.id, target_machine.id, CommunicationType.SCANNED
        )

    def _update_tcp_connections(self, src_node: Node, target_machine: Machine, event: TCPScanEvent):
        tcp_connections = set()
        open_ports = self._get_open_ports(event)
        for open_port in open_ports:
            socket_address = SocketAddress(ip=event.target, port=open_port)
            tcp_connections.add(socket_address)

        if tcp_connections:
            self._node_repository.upsert_tcp_connections(
                src_node.machine_id, {target_machine.id: tuple(tcp_connections)}
            )
