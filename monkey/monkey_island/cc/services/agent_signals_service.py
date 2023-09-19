import logging
from datetime import datetime
from typing import Optional

from common.agent_signals import AgentSignals
from common.types import AgentID
from monkey_island.cc.models import Agent, MachineID, Simulation, TerminateAllAgents
from monkey_island.cc.repositories import IAgentRepository, ISimulationRepository

logger = logging.getLogger(__name__)


class AgentSignalsService:
    def __init__(
        self, simulation_repository: ISimulationRepository, agent_repository: IAgentRepository
    ):
        self._simulation_repository = simulation_repository
        self._agent_repository = agent_repository

    def get_signals(self, agent_id: AgentID) -> AgentSignals:
        """
        Gets the signals sent to a particular agent

        :param agent_id: The ID of the agent whose signals need to be retrieved
        :return: Signals sent to the relevant agent
        """
        # NOTE: At the moment, we're not prepared to handle per-agent terminate signals. The
        #       AgentHeartbeatMonitor should set an agent-specific terminate signal when it sets
        #       the agent's stop time, which would make this logic unnecessary. For the moment, this
        #       hack represents an implicit coupling between AgentHeartbeatMonitor and
        #       AgentSignalsService. The solution is to support per-agent terminate signals.
        #
        #       The short-term solution is the below logic, which assumes that an agent which is
        #       thought to be stopped is asking if it's been terminated. This would represent an
        #       error and the agent should be signaled to stop. In the future, it can not be assumed
        #       that only agents ask about their terminate signals. If another component begins to
        #       query terminate signal times for agents, the below logic will result in an incorrect
        #       answer for any stopped agent.
        agent = self._agent_repository.get_agent_by_id(agent_id)
        if agent.stop_time is not None:
            return AgentSignals(terminate=agent.stop_time)

        if not self._agent_is_first_to_register(agent):
            return AgentSignals(terminate=agent.registration_time)

        terminate_timestamp = self._get_terminate_signal_timestamp(agent_id)
        return AgentSignals(terminate=terminate_timestamp)

    def _agent_is_first_to_register(self, agent: Agent) -> bool:
        agents_on_same_machine = self._agents_running_on_machine(agent.machine_id)
        first_to_register = min(
            agents_on_same_machine, key=lambda a: a.registration_time, default=agent
        )
        return agent.id == first_to_register.id

    def _agents_running_on_machine(self, machine_id: MachineID):
        return [
            a for a in self._agent_repository.get_running_agents() if a.machine_id == machine_id
        ]

    def _get_terminate_signal_timestamp(self, agent_id: AgentID) -> Optional[datetime]:
        simulation = self._simulation_repository.get_simulation()
        terminate_all_signal_time = simulation.terminate_signal_time
        if terminate_all_signal_time is None:
            return None

        agent = self._agent_repository.get_agent_by_id(agent_id)
        if agent.start_time <= terminate_all_signal_time:
            return terminate_all_signal_time

        progenitor = self._agent_repository.get_progenitor(agent)
        if progenitor.start_time <= terminate_all_signal_time:
            return terminate_all_signal_time

        return None

    def on_terminate_agents_signal(self, terminate_all_agents: TerminateAllAgents):
        """
        Updates the simulation repository with the terminate signal's timestamp

        :param timestamp: Timestamp of the terminate signal
        """
        timestamp = terminate_all_agents.timestamp
        updated_simulation = Simulation(terminate_signal_time=timestamp)

        self._simulation_repository.save_simulation(updated_simulation)
