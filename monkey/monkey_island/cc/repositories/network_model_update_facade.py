from functools import lru_cache
from ipaddress import IPv4Address, IPv4Interface

from monkeytypes import MachineID

from common.agent_events import AbstractAgentEvent
from common.types import AgentID
from monkey_island.cc.models import CommunicationType, Machine
from monkey_island.cc.repositories import (
    AgentMachineFacade,
    IMachineRepository,
    INodeRepository,
    UnknownRecordError,
)


class NetworkModelUpdateFacade:
    """
    A facade to simplify updating nodes and machines based on network-related events.
    """

    def __init__(
        self,
        agent_machine_facade: AgentMachineFacade,
        machine_repository: IMachineRepository,
        node_repository: INodeRepository,
    ):
        self._agent_machine_facade = agent_machine_facade
        self._machine_repository = machine_repository
        self._node_repository = node_repository

    def get_or_create_target_machine(self, target: IPv4Address) -> Machine:
        """
        Gets or creates a target machine from an IP address

        :param target: The IP address representing the target of some event
        :return: A new or existing machine that matches the target IP address
        :raises StorageError: If an error occurs while attempting to store a new machine
        :raises RetrievalError: If an error occurs while attempting to retrieve an existing machine
        """
        try:
            machine_id = self._get_machine_id_by_ip(target)
            return self._machine_repository.get_machine_by_id(machine_id)
        except UnknownRecordError:
            machine = Machine(
                id=self._machine_repository.get_new_id(),
                network_interfaces=[IPv4Interface(target)],
            )
            self._machine_repository.upsert_machine(machine)
            return machine

    @lru_cache(maxsize=1024)
    def _get_machine_id_by_ip(self, ip: IPv4Address) -> MachineID:
        machines = self._machine_repository.get_machines_by_ip(ip)

        # For now, assume that IPs are unique
        return machines[0].id

    def get_machine_id_from_agent_id(self, agent_id: AgentID) -> MachineID:
        """
        Given an AgentID, get the MachineID of the machine the Agent ran on

        :param agent_id: An AgentID
        :return: The Machine that the Agent ran on
        """
        return self._agent_machine_facade.get_machine_id_from_agent_id(agent_id)

    def upsert_communication_from_event(
        self, event: AbstractAgentEvent, communication_type: CommunicationType
    ):
        """
        Given an event and CommunicationType, update node's communication

        :param event: An event to use for source/target data. Note: target must be an IPv4Address.
        :param communication_type: The communication type that the event represents
        :raises TypeError: If event.target is not an IPv4Address
        :raises StorageError: If an error occurs while attempting to store data in one or more
                              repositories
        :raises RetrievalError: If an error occurs while attempting to retrieve data from one or
                                more repositories
        """

        if not isinstance(event.target, IPv4Address):
            raise TypeError("Event targets must be of type IPv4Address")

        source_machine_id = self._agent_machine_facade.get_machine_id_from_agent_id(event.source)
        target_machine = self.get_or_create_target_machine(event.target)

        self._node_repository.upsert_communication(
            source_machine_id, target_machine.id, communication_type
        )

    def reset_cache(self):
        self._get_machine_id_by_ip.cache_clear()
