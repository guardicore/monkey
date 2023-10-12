from ipaddress import IPv4Address
from itertools import count
from threading import Lock
from typing import Any, Sequence

from pymongo import MongoClient

from common.types import HardwareID
from monkey_island.cc.models import Machine, MachineID, NetworkServices

from . import IMachineRepository, RemovalError, RetrievalError, StorageError, UnknownRecordError
from .consts import MONGO_OBJECT_ID_KEY
from .utils import mongo_dot_decoder, mongo_dot_encoder


class MongoMachineRepository(IMachineRepository):
    """A repository used to store and retrieve Machines in MongoDB"""

    def __init__(self, mongo_client: MongoClient):
        self._machines_collection = mongo_client.monkey_island.machines
        self._id_lock = Lock()
        self._id_iterator = count(start=(self._get_biggest_id() + 1))

    def _get_biggest_id(self) -> MachineID:
        try:
            return self._machines_collection.find().sort("id", -1).limit(1)[0]["id"]
        except IndexError:
            return 0

    def get_new_id(self) -> MachineID:
        with self._id_lock:
            return next(self._id_iterator)

    def upsert_machine(self, machine: Machine):
        try:
            machine_dict = mongo_dot_encoder(machine.model_dump(mode="json"))
            result = self._machines_collection.replace_one(
                {"id": machine.id}, machine_dict, upsert=True
            )
        except Exception as err:
            raise StorageError(f'Error updating machine with ID "{machine.id}": {err}')

        if result.matched_count == 0 and result.upserted_id is None:
            raise StorageError(
                f'Error inserting machine with ID "{machine.id}": Expected to insert 1 machine, '
                f"but no machines were inserted"
            )

    def upsert_network_services(self, machine_id: MachineID, services: NetworkServices):
        machine = self.get_machine_by_id(machine_id)
        try:
            machine.network_services.update(services)
            self.upsert_machine(machine)
        except Exception as err:
            raise StorageError("Failed upserting the machine or adding services") from err

    def get_machine_by_id(self, machine_id: MachineID) -> Machine:
        return self._find_one("id", machine_id)

    def get_machine_by_hardware_id(self, hardware_id: HardwareID) -> Machine:
        return self._find_one("hardware_id", hardware_id)

    def _find_one(self, key: str, search_value: Any) -> Machine:
        try:
            machine_dict = self._machines_collection.find_one(
                {key: search_value}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise RetrievalError(f'Error retrieving machine with "{key} == {search_value}": {err}')

        if machine_dict is None:
            raise UnknownRecordError(f'Unknown machine with "{key} == {search_value}"')

        machine_dict = mongo_dot_decoder(machine_dict)
        return Machine(**machine_dict)

    def get_machines(self) -> Sequence[Machine]:
        try:
            cursor = self._machines_collection.find({}, {MONGO_OBJECT_ID_KEY: False})
        except Exception as err:
            raise RetrievalError(f"Error retrieving machines: {err}")

        return [Machine(**mongo_dot_decoder(m)) for m in cursor]

    def get_machines_by_ip(self, ip: IPv4Address) -> Sequence[Machine]:
        ip_regex = "^" + str(mongo_dot_encoder(str(ip))) + "\\/.*$"
        query = {"network_interfaces": {"$elemMatch": {"$regex": ip_regex}}}

        try:
            cursor = self._machines_collection.find(query, {MONGO_OBJECT_ID_KEY: False})
        except Exception as err:
            raise RetrievalError(f'Error retrieving machines with ip "{ip}": {err}')

        machines = [Machine(**mongo_dot_decoder(m)) for m in cursor]

        if len(machines) == 0:
            raise UnknownRecordError(f'No machines found with IP "{ip}"')

        return machines

    def reset(self):
        try:
            self._machines_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")
