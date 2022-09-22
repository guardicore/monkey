from datetime import datetime

from monkey_island.cc.models import Agent, AgentSignals
from monkey_island.cc.repository import ISimulationRepository


class AgentSignalsService:
    def __init__(self, simulation_repository: ISimulationRepository):
        self._simulation_repository = simulation_repository

    def get_signals(self, agent: Agent) -> AgentSignals:
        """
        Gets the signals sent to a particular agent

        :param agent: The agent whose signals need to be retrieved
        :return: Signals sent to the relevant agent
        """
        return AgentSignals(timestamp=datetime.now())

    def on_terminate_agents_signal(self, timestamp: datetime):
        """
        Updates the simulation repository with the terminate signal's timestamp

        :param timestamp: Timestamp of the terminate signal
        """
        pass
