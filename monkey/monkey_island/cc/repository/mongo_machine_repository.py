from ipaddress import IPv4Address
from threading import Lock
from typing import Any, MutableMapping, Sequence

from pymongo import MongoClient

from common.types import HardwareID
from monkey_island.cc.models import Machine, MachineID

from . import IMachineRepository, RetrievalError, StorageError, UnknownRecordError
from .consts import MONGO_OBJECT_ID_KEY


class MongoMachineRepository(IMachineRepository):
    """A repository used to store and retrieve Machines in MongoDB"""

    def __init__(self, mongo_client: MongoClient):
        self._machines_collection = mongo_client.monkey_island.machines
        self._id_lock = Lock()
        self._next_id = self._get_biggest_id()

    def _get_biggest_id(self) -> MachineID:
        try:
            return self._machines_collection.find().sort("id", -1).limit(1)[0]["id"]
        except IndexError:
            return 0

    def create_machine(self) -> Machine:
        try:
            next_id = self._get_next_id()
            new_machine = Machine(id=next_id)
            self._machines_collection.insert_one(new_machine.dict(simplify=True))

            return new_machine
        except Exception as err:
            raise StorageError(f"Error creating a new machine: {err}")

    def _get_next_id(self) -> MachineID:
        with self._id_lock:
            self._next_id += 1
            return self._next_id

    def update_machine(self, machine: Machine):
        try:
            result = self._machines_collection.replace_one(
                {"id": machine.id}, machine.dict(simplify=True)
            )
        except Exception as err:
            raise StorageError(f'Error updating machine with ID "{machine.id}": {err}')

        if result.matched_count == 0:
            raise UnknownRecordError(f"Unknown machine: id == {machine.id}")

        if result.modified_count != 1:
            raise StorageError(
                f'Error updating machine with ID "{machine.id}": Expected to update 1 machines, '
                f"but updated {result.modified_count}"
            )

    def get_machine_by_id(self, id_: MachineID) -> Machine:
        return self._find_one("id", "machine ID", id_)

    def get_machine_by_hardware_id(self, hardware_id: HardwareID) -> Machine:
        return self._find_one("hardware_id", "hardware ID", hardware_id)

    def _find_one(self, key: str, key_display_name: str, search_value: Any) -> Machine:
        try:
            machine_dict = self._machines_collection.find_one({key: search_value})
        except Exception as err:
            raise RetrievalError(f'Error retrieving machine with "{key} == {search_value}": {err}')

        if machine_dict is None:
            raise UnknownRecordError(f'Unknown {key_display_name} "{search_value}"')

        return MongoMachineRepository._mongo_record_to_machine(machine_dict)

    def get_machines_by_ip(self, ip: IPv4Address) -> Sequence[Machine]:
        ip_regex = "^" + str(ip).replace(".", "\\.") + "\\/.*$"
        query = {"network_interfaces": {"$elemMatch": {"$regex": ip_regex}}}

        try:
            cursor = self._machines_collection.find(query)
        except Exception as err:
            raise RetrievalError(f'Error retrieving machines with ip "{ip}": {err}')

        machines = list(map(MongoMachineRepository._mongo_record_to_machine, cursor))

        if len(machines) == 0:
            raise UnknownRecordError(f'No machines found with IP "{ip}"')

        return machines

    @staticmethod
    def _mongo_record_to_machine(mongo_record: MutableMapping[str, Any]) -> Machine:
        del mongo_record[MONGO_OBJECT_ID_KEY]
        return Machine(**mongo_record)

    def reset(self):
        self._machines_collection.drop()
