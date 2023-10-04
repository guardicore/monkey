from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence

from monkeytypes import AgentPluginManifest, AgentPluginType, OperatingSystem

from common import AgentRegistrationData, AgentSignals
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin
from common.credentials import Credentials


class IIslandAPIClient(ABC):
    """
    A client for the Island's API
    """

    @abstractmethod
    def login(self, otp: str):
        """
        Connect to the island's API

        :param otp: A one-time password used to authenticate with the Island API
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the Island
        :raises IslandAPIRequestError: If an error occurs while attempting to login to the
                                       Island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to login to the
                                             Island API due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the Island
        :raises IslandAPIError: If an unexpected error occurs while attempting to login to the
                                Island API
        """

    @abstractmethod
    def logout(self):
        """
        Disconnect from the island's API

        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the Island
        :raises IslandAPIRequestError: If an error occurs while attempting to logout from the
                                       Island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to logout from the
                                             Island API due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the Island
        :raises IslandAPIError: If an unexpected error occurs while attempting to logout from the
                                Island API
        """

    @abstractmethod
    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        """
        Get an agent binary for the given OS from the island

        :param operating_system: The OS on which the agent binary will run
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
    def get_otp(self) -> str:
        """
        Get a one-time password (OTP) for an Agent so it can authenticate with the Island

        :raises IslandAPIAuthenticationError: If authentication fails
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the Island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       Island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             Island due to an error on the server
        :raises IslandAPIRequestLimitExceededError: If the request limit for OTPs has been exceeded
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the Island
        :raises IslandAPIError: If an unexpected error occurs while attempting to get an OTP
        :return: The OTP
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
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
        :raises IslandAPIConnectionError: If the client could not connect to the island
        :raises IslandAPIRequestError: If there was a problem with the client request
        :raises IslandAPIRequestFailedError: If the server experienced an error
        :raises IslandAPITimeoutError: If the command timed out
        :return: The agent plugin manifest
        """

    @abstractmethod
    def get_agent_signals(self) -> AgentSignals:
        """
        Gets the agent's signals from the island

        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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

        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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

        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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

        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
    def send_heartbeat(self, timestamp: float):
        """
        Send a "heartbeat" to the Island to indicate that the agent is still alive

        :param timestamp: The timestamp of the agent's heartbeat
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
    def send_log(self, log_contents: str):
        """
        Send the contents of the agent's log to the island

        :param log_contents: The contents of the agent's log
        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
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
    def terminate_signal_is_set(self) -> bool:
        """
        Checks if the agent's terminate signal is set

        :raises IslandAPIAuthenticationError: If the client is not authorized to access this
                                              endpoint
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to send the
                                contents of the agent's log to the island
        """
