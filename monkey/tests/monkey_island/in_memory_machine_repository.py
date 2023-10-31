from ipaddress import IPv4Address
from typing import Dict, Sequence

from monkeytypes import MachineID

from common.types import HardwareID
from monkey_island.cc.models import Machine, NetworkServices
from monkey_island.cc.repositories import IMachineRepository, UnknownRecordError


class InMemoryMachineRepository(IMachineRepository):
    def __init__(self, seed_id: MachineID = 1):
        self._machines: Dict[MachineID, Machine] = {}
        self._next_id = seed_id

    def get_new_id(self) -> MachineID:
        self._next_id += 1
        return self._next_id - 1

    def upsert_machine(self, machine: Machine):
        self._machines[machine.id] = machine

    def upsert_network_services(self, machine_id: MachineID, services: NetworkServices):
        try:
            machine = self._machines[machine_id]
        except KeyError:
            raise UnknownRecordError(f"Unknown machine {machine_id}")

        machine.network_services.update(services)

        self.upsert_machine(machine)

    def get_machine_by_id(self, machine_id: MachineID) -> Machine:
        try:
            return self._machines[machine_id]
        except KeyError:
            raise UnknownRecordError(f"Unknown machine {machine_id}")

    def get_machine_by_hardware_id(self, hardware_id: HardwareID) -> Machine:
        for machine in self._machines:
            if machine.hardware_id == hardware_id:
                return machine

        raise UnknownRecordError(f"Unknown machine with hardware ID {hardware_id}")

    def get_machines(self) -> Sequence[Machine]:
        return list(self._machines.values())

    def get_machines_by_ip(self, ip: IPv4Address) -> Sequence[Machine]:
        matching_machines = []
        for machine in self._machines.values():
            for interface in machine.network_interfaces:
                if interface.ip == ip:
                    matching_machines.append(machine)
                    break

        if not matching_machines:
            raise UnknownRecordError(f"Unknown machine with IP {ip}")

        return matching_machines

    def reset(self):
        self._machines = {}
