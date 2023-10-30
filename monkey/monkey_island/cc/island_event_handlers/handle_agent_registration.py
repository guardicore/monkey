from contextlib import suppress
from datetime import datetime
from ipaddress import IPv4Interface
from typing import Callable, List, Optional

from monkeytypes import SocketAddress

from common import AgentRegistrationData
from monkey_island.cc.models import Agent, CommunicationType, Machine
from monkey_island.cc.repositories import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    UnknownRecordError,
)


class handle_agent_registration:
    """
    Update repositories when a new agent registers
    """

    def __init__(
        self,
        machine_repository: IMachineRepository,
        agent_repository: IAgentRepository,
        node_repository: INodeRepository,
        get_current_datetime: Callable[[], datetime] = datetime.now,
    ):
        self._machine_repository = machine_repository
        self._agent_repository = agent_repository
        self._node_repository = node_repository
        self._get_current_datetime = get_current_datetime

    def __call__(self, agent_registration_data: AgentRegistrationData):
        machine = self._update_machine_repository(agent_registration_data)
        self._add_agent(agent_registration_data, machine)
        self._add_node_communication(agent_registration_data, machine)

    def _update_machine_repository(self, agent_registration_data: AgentRegistrationData) -> Machine:
        machine = self._find_existing_machine_to_update(agent_registration_data)

        if machine is None:
            machine = Machine(id=self._machine_repository.get_new_id())

        self._upsert_machine(machine, agent_registration_data)

        return machine

    def _find_existing_machine_to_update(
        self, agent_registration_data: AgentRegistrationData
    ) -> Optional[Machine]:
        with suppress(UnknownRecordError):
            return self._machine_repository.get_machine_by_hardware_id(
                agent_registration_data.machine_hardware_id
            )

        for network_interface in agent_registration_data.network_interfaces:
            with suppress(UnknownRecordError):
                # NOTE: For now, assume IPs are unique. In reality, two machines could share the
                #       same IP if there's a router between them.
                return self._machine_repository.get_machines_by_ip(network_interface.ip)[0]

        return None

    def _upsert_machine(self, machine: Machine, agent_registration_data: AgentRegistrationData):
        self._update_hardware_id(machine, agent_registration_data)
        self._update_network_interfaces(machine, agent_registration_data)

        self._machine_repository.upsert_machine(machine)

    def _update_hardware_id(self, machine: Machine, agent_registration_data: AgentRegistrationData):
        if (
            machine.hardware_id is not None
            and machine.hardware_id != agent_registration_data.machine_hardware_id
        ):
            raise Exception(
                f"Hardware ID mismatch:\n\tMachine: {machine}\n\t"
                f"AgentRegistrationData: {agent_registration_data}"
            )

        machine.hardware_id = agent_registration_data.machine_hardware_id

    def _update_network_interfaces(
        self, machine: Machine, agent_registration_data: AgentRegistrationData
    ):
        updated_network_interfaces: List[IPv4Interface] = []
        agent_registration_data_ips = set(
            map(lambda iface: iface.ip, agent_registration_data.network_interfaces)
        )

        # Prefer interfaces provided by the AgentRegistrationData to those in the Machine record.
        # The AgentRegistrationData was collected while running on the machine, whereas the Machine
        # data may have only been collected from a scan. For example, the Machine and
        # AgentRedistrationData may have the same IP with a different subnet mask.
        for interface in machine.network_interfaces:
            if interface.ip not in agent_registration_data_ips:
                updated_network_interfaces.append(interface)

        updated_network_interfaces.extend(agent_registration_data.network_interfaces)

        machine.network_interfaces = sorted(updated_network_interfaces)

    def _add_agent(self, agent_registration_data: AgentRegistrationData, machine: Machine):
        new_agent = Agent(
            id=agent_registration_data.id,
            machine_id=machine.id,
            registration_time=self._get_current_datetime(),
            start_time=agent_registration_data.start_time,
            parent_id=agent_registration_data.parent_id,
            cc_server=agent_registration_data.cc_server,
            sha256=agent_registration_data.sha256,
        )
        self._agent_repository.upsert_agent(new_agent)

    def _add_node_communication(
        self, agent_registration_data: AgentRegistrationData, src_machine: Machine
    ):
        dst_machine = self._get_or_create_cc_machine(agent_registration_data.cc_server)

        self._node_repository.upsert_communication(
            src_machine.id, dst_machine.id, CommunicationType.CC
        )

    def _get_or_create_cc_machine(self, cc_server: SocketAddress) -> Machine:
        dst_ip = cc_server.ip

        try:
            return self._machine_repository.get_machines_by_ip(dst_ip)[0]
        except UnknownRecordError:
            new_machine = Machine(
                id=self._machine_repository.get_new_id(), network_interfaces=[IPv4Interface(dst_ip)]
            )
            self._machine_repository.upsert_machine(new_machine)

            return new_machine
