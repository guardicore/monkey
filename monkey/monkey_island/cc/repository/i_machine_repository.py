from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import Sequence

from common.types import HardwareID
from monkey_island.cc.models import Machine, MachineID


class IMachineRepository(ABC):
    """A repository used to store and retrieve Machines"""

    @abstractmethod
    def get_new_id(self) -> MachineID:
        """
        Generates a new, unique `MachineID`

        :return: A new, unique `MachineID`
        """

    @abstractmethod
    def upsert_machine(self, machine: Machine):
        """
        Upsert (insert or update) a `Machine`

        Insert the `Machine` if no `Machine` with a matching ID exists in the repository. If the
        `Machine` already exists, update it.

        :param machine: The `Machine` to be inserted or updated
        :raises StorageError: If an error occurs while attempting to store the `Machine`
        """

    @abstractmethod
    def get_machine_by_id(self, machine_id: MachineID) -> Machine:
        """
        Get a `Machine` by ID

        :param machine_id: The ID of the `Machine` to be retrieved
        :return: A `Machine` with a matching `id`
        :raises UnknownRecordError: If a `Machine` with the specified `id` does not exist in the
                                    repository
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Machine`
        """

    @abstractmethod
    def get_machine_by_hardware_id(self, hardware_id: HardwareID) -> Machine:
        """
        Get a `Machine` by ID

        :param hardware_id: The hardware ID of the `Machine` to be retrieved
        :return: A `Machine` with a matching `hardware_id`
        :raises UnknownRecordError: If a `Machine` with the specified `hardware_id` does not exist
                                    in the repository
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Machine`
        """

    @abstractmethod
    def get_machines_by_ip(self, ip: IPv4Address) -> Sequence[Machine]:
        """
        Search for machines by IP address

        :param ip: The IP address to search for
        :return: A sequence of Machines that have a network interface with a matching IP
        :raises UnknownRecordError: If a `Machine` with the specified `ip` does not exist in the
                                    repository
        :raises RetrievalError: If an error occurs while attempting to retrieve the `Machine`
        """

    @abstractmethod
    def reset(self):
        """
        Removes all data from the repository

        :raises RemovalError: If an error occurs while attempting to remove all `Machines` from
                              the repository
        """
