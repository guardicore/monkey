from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import Sequence

from common.types import HardwareID
from monkey_island.cc.models import Machine, MachineID


class IMachineRepository(ABC):
    """A repository used to store and retrieve Machines"""

    @abstractmethod
    def create_machine(self) -> Machine:
        """
        Create a new `Machine` in the repository

        :return: A new `Machine` with a unique ID
        :raises StorageError: If a new `Machine` could not be created
        """

    @abstractmethod
    def update_machine(self, machine: Machine):
        """
        Update an existing `Machine` in the repository

        :param machine: An updated Machine object to store in the repository
        :raises UnknownRecordError: If the provided `Machine` does not exist in the repository
        :raises StorageError: If an error occurred while attempting to store the `Machine`
        """

    @abstractmethod
    def get_machine_by_id(self, id_: MachineID) -> Machine:
        """
        Get a `Machine` by ID

        :param id: The ID of the `Machine` to be retrieved
        :return: A `Machine` with a matching `id`
        :raises UnknownRecordError: If a `Machine` with the specified `id` does not exist in the
                                    repository
        :raises RetrievalError: If an error occurred while attempting to retrieve the `Machine`
        """

    @abstractmethod
    def get_machine_by_hardware_id(self, hardware_id: HardwareID) -> Machine:
        """
        Get a `Machine` by ID

        :param hardware_id: The hardware ID of the `Machine` to be retrieved
        :return: A `Machine` with a matching `hardware_id`
        :raises UnknownRecordError: If a `Machine` with the specified `hardware_id` does not exist
                                    in the repository
        :raises RetrievalError: If an error occurred while attempting to retrieve the `Machine`
        """

    @abstractmethod
    def get_machines_by_ip(self, ip: IPv4Address) -> Sequence[Machine]:
        """
        Search for machines by IP address

        :param ip: The IP address to search for
        :return: A sequence of Machines that have a network interface with a matching IP
        :raises UnknownRecordError: If a `Machine` with the specified `ip` does not exist in the
                                    repository
        :raises RetrievalError: If an error occurred while attempting to retrieve the `Machine`
        """

    @abstractmethod
    def reset(self):
        """
        Removes all data from the repository
        """
