from contextlib import suppress
from typing import Optional

from common import AgentRegistrationData
from monkey_island.cc.models import Agent, Machine
from monkey_island.cc.repository import IAgentRepository, IMachineRepository, UnknownRecordError


class handle_agent_registration:
    """
    Update repositories when a new agent registers
    """

    def __init__(self, machine_repository: IMachineRepository, agent_repository: IAgentRepository):
        self._machine_repository = machine_repository
        self._agent_repository = agent_repository

    def __call__(self, agent_registration_data: AgentRegistrationData):
        machine = self._update_machine_repository(agent_registration_data)
        self._add_agent(agent_registration_data, machine)

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

    def _upsert_machine(
        self, existing_machine: Machine, agent_registration_data: AgentRegistrationData
    ):
        updated_machine = existing_machine.copy()

        self._update_hardware_id(updated_machine, agent_registration_data)
        self._update_network_interfaces(updated_machine, agent_registration_data)

        self._machine_repository.upsert_machine(updated_machine)

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
        updated_network_interfaces = set(machine.network_interfaces)
        updated_network_interfaces = updated_network_interfaces.union(
            agent_registration_data.network_interfaces
        )

        machine.network_interfaces = sorted(updated_network_interfaces)

    def _add_agent(self, agent_registration_data: AgentRegistrationData, machine: Machine):
        new_agent = Agent(
            id=agent_registration_data.id,
            machine_id=machine.id,
            start_time=agent_registration_data.start_time,
            parent_id=agent_registration_data.parent_id,
            cc_server=agent_registration_data.cc_server,
        )
        self._agent_repository.upsert_agent(new_agent)
