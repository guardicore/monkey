from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence

from common import AgentRegistrationData, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.credentials import Credentials


class IIslandAPIClient(ABC):
    """
    A client for the Island's API
    """

    @abstractmethod
    def connect(self, island_server: str):
        """
        Connect to the island's API

        :param island_server: The socket address of the API
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to connect to the
                                island
        """

    @abstractmethod
    def send_log(self, log_contents: str):
        """
        Send the contents of the agent's log to the island

        :param log_contents: The contents of the agent's log
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to send the
                                contents of the agent's log to the island
        """

    @abstractmethod
    def get_pba_file(self, filename: str) -> bytes:
        """
        Get a custom PBA file from the island

        :param filename: The name of the custom PBA file
        :return: The contents of the custom PBA file in bytes
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to retrieve the
                                custom PBA file
        """

    @abstractmethod
    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        """
        Get an agent binary for the given OS from the island

        :param operating_system: The OS on which the agent binary will run
        :return: The agent binary file
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to retrieve the
                                agent binary
        """

    @abstractmethod
    def send_events(self, events: Sequence[AbstractAgentEvent]):
        """
        Send a sequence of agent events to the Island

        :param events: A sequence of agent events
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to send events to
                                the island
        """

    @abstractmethod
    def register_agent(self, agent_registration_data: AgentRegistrationData):
        """
        Register an agent with the Island

        :param agent_registration_data: Information about the agent to register
            with the island
        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        """

    @abstractmethod
    def get_config(self) -> AgentConfiguration:
        """
        Get agent configuration from the island

        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: Agent configuration
        """

    @abstractmethod
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        """
        Get credentials from the island

        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: Credentials
        """

    @abstractmethod
    def get_agent_signals(self, agent_id: str) -> Optional[datetime]:
        """
        Gets an agent's signals from the island

        :param agent_id: ID of the agent whose signals should be retrieved
        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: The relevant agent's terminate signal's timestamp
        """
