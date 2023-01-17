from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from common.credentials import Credentials
from common.types import AgentID, SocketAddress


class IIslandAPIClient(ABC):
    """
    A client for the Island's API
    """

    @abstractmethod
    def connect(self, island_server: SocketAddress):
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
    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        """
        Get an agent binary for the given OS from the island

        :param operating_system: The OS on which the agent binary will run
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to retrieve the
                                agent binary
        :return: The agent binary file
        """

    @abstractmethod
    def get_agent_plugin(
        self, operating_system: OperatingSystem, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPlugin:
        """
        Gets plugin from the Island based on plugin type and name

        :param operating_system: The OS on which the plugin will run
        :param plugin_type: Type of plugin to be fetched
        :param plugin_name: Name of plugin to be fetched
        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: The agent plugin
        """

    @abstractmethod
    def get_agent_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPluginManifest:
        """
        Gets the manifest of a plugin

        :param plugin_type: Type of the plugin
        :param plugin_name: Name of the plugin
        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: The agent plugin manifest
        """

    @abstractmethod
    def get_agent_signals(self, agent_id: str) -> AgentSignals:
        """
        Gets an agent's signals from the island

        :param agent_id: ID of the agent whose signals should be retrieved
        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: The relevant agent's signals
        """

    @abstractmethod
    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        """
        Gets the agent configuration schema from the island

        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: The agent configuration schema
        """

    @abstractmethod
    def get_config(self) -> AgentConfiguration:
        """
        Get agent configuration from the island

        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :raises IslandAPIError: If an unexpected error occurs while attempting to get the
                                configuration from the island
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
    def send_heartbeat(self, agent: AgentID, timestamp: float):
        """
        Send a "heartbeat" to the Island to indicate that the agent is still alive

        :param agent_id: The ID of the agent who is sending a heartbeat
        :param timestamp: The timestamp of the agent's heartbeat
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to send the
                                agent heartbeat to the island
        """

    @abstractmethod
    def send_log(self, agent_id: AgentID, log_contents: str):
        """
        Send the contents of the agent's log to the island

        :param agent_id: The ID of the agent whose logs are being sent
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
