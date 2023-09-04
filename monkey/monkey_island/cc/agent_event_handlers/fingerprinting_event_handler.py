from common.agent_events import FingerprintingEvent
from common.types import SocketAddress
from monkey_island.cc.models import Machine, NetworkServices
from monkey_island.cc.repositories import IMachineRepository, NetworkModelUpdateFacade


class FingerprintingEventHandler:
    """
    Handles fingerprinting event and makes changes to Machine based on it
    """

    def __init__(
        self,
        network_model_update_facade: NetworkModelUpdateFacade,
        machine_repository: IMachineRepository,
    ):
        self._network_model_update_facade = network_model_update_facade
        self._machine_repository = machine_repository

    def handle_fingerprinting_event(self, event: FingerprintingEvent):
        target_machine = self._network_model_update_facade.get_or_create_target_machine(
            event.target
        )

        self._update_target_machine_os(target_machine, event)
        self._update_target_machine_os_version(target_machine, event)
        self._update_machine_network_services(target_machine, event)

    def _update_target_machine_os(self, machine: Machine, event: FingerprintingEvent):
        if event.os is not None and machine.operating_system is None:
            machine.operating_system = event.os
            self._machine_repository.upsert_machine(machine)

    def _update_target_machine_os_version(self, machine: Machine, event: FingerprintingEvent):
        if event.os_version is not None and machine.operating_system_version == "":
            machine.operating_system_version = event.os_version
            self._machine_repository.upsert_machine(machine)

    def _update_machine_network_services(self, machine: Machine, event: FingerprintingEvent):
        network_services = self._get_new_network_services_from_event(event)
        if network_services:
            self._machine_repository.upsert_network_services(machine.id, network_services)

    @classmethod
    def _get_new_network_services_from_event(cls, event: FingerprintingEvent) -> NetworkServices:
        new_services: NetworkServices = {}

        for discovered_service in event.discovered_services:
            socket_address = SocketAddress(ip=event.target, port=discovered_service.port)
            new_services[socket_address] = discovered_service.service

        return new_services
