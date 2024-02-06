from abc import ABC, abstractmethod

from agentpluginapi import IAgentOTPProvider
from monkeytypes import AgentID

from .i_linux_agent_command_builder import ILinuxAgentCommandBuilder
from .i_windows_agent_command_builder import IWindowsAgentCommandBuilder
from .linux_agent_command_builder import LinuxAgentCommandBuilder
from .windows_agent_command_builder import WindowsAgentCommandBuilder


class IAgentCommandBuilderFactory(ABC):
    @abstractmethod
    def create_linux_agent_command_builder(
        self,
    ) -> ILinuxAgentCommandBuilder:
        """
        Builds an ILinuxAgentCommandBuilder that construct the Agent command
        """

    @abstractmethod
    def create_windows_agent_command_builder(
        self,
    ) -> IWindowsAgentCommandBuilder:
        """
        Builds an IWindowsAgentCommandBuilder that construct the Agent command
        """


class AgentCommandBuilderFactory(IAgentCommandBuilderFactory):
    def __init__(
        self,
        agent_id: AgentID,
        servers: list[str],
        otp_provider: IAgentOTPProvider,
        agent_otp_environment_variable: str,
        current_depth: int = 0,
    ):
        self._agent_id = agent_id
        self._servers = servers
        self._otp_provider = otp_provider
        self._agent_otp_environment_variable = agent_otp_environment_variable
        self._current_depth = current_depth

    def create_linux_agent_command_builder(
        self,
    ) -> ILinuxAgentCommandBuilder:
        return LinuxAgentCommandBuilder(
            self._agent_id,
            self._servers,
            self._otp_provider,
            self._agent_otp_environment_variable,
            self._current_depth,
        )

    def create_windows_agent_command_builder(
        self,
    ) -> IWindowsAgentCommandBuilder:
        return WindowsAgentCommandBuilder(
            self._agent_id,
            self._servers,
            self._otp_provider,
            self._agent_otp_environment_variable,
            self._current_depth,
        )
