from ipaddress import IPv4Address, IPv4Interface

from monkey_island.cc.models import Machine
from monkey_island.cc.repository import IMachineRepository, UnknownRecordError


def get_or_create_target_machine(repository: IMachineRepository, target: IPv4Address):
    try:
        target_machines = repository.get_machines_by_ip(target)
        return target_machines[0]
    except UnknownRecordError:
        machine = Machine(
            id=repository.get_new_id(),
            network_interfaces=[IPv4Interface(target)],
        )
        repository.upsert_machine(machine)
        return machine
