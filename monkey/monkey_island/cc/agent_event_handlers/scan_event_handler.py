from logging import getLogger
from typing import List, Sequence, Union

from typing_extensions import TypeAlias

from common.agent_events import PingScanEvent, TCPScanEvent
from common.types import NetworkPort, NetworkService, PortStatus, SocketAddress
from monkey_island.cc.models import CommunicationType, Machine, NetworkServices
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

from .node_update_facade import NodeUpdateFacade

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
        self._node_update_facade = NodeUpdateFacade(
            agent_repository, machine_repository, node_repository
        )
        self._agent_repository = agent_repository
        self._machine_repository = machine_repository
        self._node_repository = node_repository

    def handle_ping_scan_event(self, event: PingScanEvent):
        if not event.response_received:
            return

        try:
            target_machine = self._get_target_machine(event)

            self._update_target_machine_os(target_machine, event)
            self._node_update_facade.upsert_communication_from_event(
                event, CommunicationType.SCANNED
            )
        except (RetrievalError, StorageError, UnknownRecordError):
            logger.exception("Unable to process ping scan data")

    def _get_target_machine(self, event: ScanEvent) -> Machine:
        return self._node_update_facade.get_or_create_target_machine(event.target)

    def handle_tcp_scan_event(self, event: TCPScanEvent):
        num_open_ports = len(self._get_open_ports(event))

        if num_open_ports <= 0:
            return

        try:
            tcp_connections = self._get_tcp_connections_from_event(event)
            network_services = self._get_network_services_from_event(event)

            self._upsert_from_tcp_scan_event(event, tcp_connections, network_services)
        except (RetrievalError, StorageError, UnknownRecordError):
            logger.exception("Unable to process tcp scan data")

    @staticmethod
    def _get_open_ports(event: TCPScanEvent) -> List[NetworkPort]:
        return [port for port, status in event.ports.items() if status == PortStatus.OPEN]

    def _update_target_machine_os(self, machine: Machine, event: PingScanEvent):
        if event.os is not None and machine.operating_system is None:
            machine.operating_system = event.os
            self._machine_repository.upsert_machine(machine)

    @classmethod
    def _get_tcp_connections_from_event(cls, event: TCPScanEvent) -> Sequence[SocketAddress]:
        tcp_connections = set()
        open_ports = cls._get_open_ports(event)
        for open_port in open_ports:
            socket_address = SocketAddress(ip=event.target, port=open_port)
            tcp_connections.add(socket_address)

        return tuple(tcp_connections)

    @classmethod
    def _get_network_services_from_event(cls, event: TCPScanEvent) -> NetworkServices:
        return {
            SocketAddress(ip=event.target, port=port): NetworkService.UNKNOWN
            for port in cls._get_open_ports(event)
        }

    def _upsert_from_tcp_scan_event(
        self,
        event: TCPScanEvent,
        tcp_connections: Sequence[SocketAddress],
        network_services: NetworkServices,
    ):
        source_machine_id = self._node_update_facade.get_machine_id_from_agent_id(event.source)
        target_machine = self._node_update_facade.get_or_create_target_machine(event.target)

        self._node_repository.upsert_communication(
            source_machine_id, target_machine.id, CommunicationType.SCANNED
        )

        self._node_repository.upsert_tcp_connections(
            source_machine_id, {target_machine.id: tuple(tcp_connections)}
        )

        self._machine_repository.upsert_network_services(target_machine.id, network_services)
