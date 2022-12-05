import logging
from datetime import datetime
from typing import Optional

from common.agent_signals import AgentSignals
from common.types import AgentID
from monkey_island.cc.models import Simulation, TerminateAllAgents
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
        terminate_timestamp = self._get_terminate_signal_timestamp(agent_id)
        return AgentSignals(terminate=terminate_timestamp)

    def _get_terminate_signal_timestamp(self, agent_id: AgentID) -> Optional[datetime]:
        agent = self._agent_repository.get_agent_by_id(agent_id)
        if agent.stop_time is not None:
            return agent.stop_time

        simulation = self._simulation_repository.get_simulation()
        terminate_all_signal_time = simulation.terminate_signal_time
        if terminate_all_signal_time is None:
            return None

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
        simulation = self._simulation_repository.get_simulation()
        timestamp = terminate_all_agents.timestamp
        updated_simulation = Simulation(mode=simulation.mode, terminate_signal_time=timestamp)

        self._simulation_repository.save_simulation(updated_simulation)
