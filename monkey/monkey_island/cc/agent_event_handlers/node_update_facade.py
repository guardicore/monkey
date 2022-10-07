from ipaddress import IPv4Address, IPv4Interface

from monkey_island.cc.models import Machine
from monkey_island.cc.repository import IMachineRepository, UnknownRecordError


class NodeUpdateFacade:
    def __init__(self, machine_repository: IMachineRepository):
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
