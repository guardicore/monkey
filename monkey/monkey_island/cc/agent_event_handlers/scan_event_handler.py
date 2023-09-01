from logging import getLogger
from typing import List, Sequence

from common.agent_events import PingScanEvent, TCPScanEvent
from common.types import NetworkPort, NetworkService, PortStatus, SocketAddress
from monkey_island.cc.models import CommunicationType, Machine, NetworkServices
from monkey_island.cc.repositories import (
    IMachineRepository,
    INodeRepository,
    NetworkModelUpdateFacade,
)

logger = getLogger(__name__)


# TODO: Split this up into separate TCP handler and Ping handler. When these were merged together,
#       they were doing basically the same thing. Now they're not.
#
#       Pass a `NodeUpdateFacade` into the constructor instead of building one. Register
#       `NodeUpdateFacade` with the DIContainer. Then simplify the unit tests.
class ScanEventHandler:
    """
    Handles scan event and makes changes to Machine and Node states based on it
    """

    def __init__(
        self,
        network_model_update_facade: NetworkModelUpdateFacade,
        machine_repository: IMachineRepository,
        node_repository: INodeRepository,
    ):
        self._network_model_update_facade = network_model_update_facade
        self._machine_repository = machine_repository
        self._node_repository = node_repository

    def handle_ping_scan_event(self, event: PingScanEvent):
        if not event.response_received:
            return

        target_machine = self._network_model_update_facade.get_or_create_target_machine(
            event.target
        )
        self._update_target_machine_os(target_machine, event)

        self._network_model_update_facade.upsert_communication_from_event(
            event, CommunicationType.SCANNED
        )

    def _update_target_machine_os(self, machine: Machine, event: PingScanEvent):
        if event.os is not None and machine.operating_system is None:
            machine.operating_system = event.os
            self._machine_repository.upsert_machine(machine)

    def handle_tcp_scan_event(self, event: TCPScanEvent):
        num_open_ports = len(self._get_open_ports(event))

        if num_open_ports <= 0:
            return

        tcp_connections = self._get_tcp_connections_from_event(event)
        network_services = self._get_network_services_from_event(event)

        self._upsert_from_tcp_scan_event(event, tcp_connections, network_services)

    @staticmethod
    def _get_open_ports(event: TCPScanEvent) -> List[NetworkPort]:
        return [port for port, status in event.ports.items() if status == PortStatus.OPEN]

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
        source_machine_id = self._network_model_update_facade.get_machine_id_from_agent_id(
            event.source
        )
        target_machine = self._network_model_update_facade.get_or_create_target_machine(
            event.target
        )

        self._node_repository.upsert_communication(
            source_machine_id, target_machine.id, CommunicationType.SCANNED
        )

        self._node_repository.upsert_tcp_connections(
            source_machine_id, {target_machine.id: tuple(tcp_connections)}
        )

        self._machine_repository.upsert_network_services(target_machine.id, network_services)
