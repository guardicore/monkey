from abc import ABC, abstractmethod

from agentpluginapi import IAgentOTPProvider, TargetHost
from monkeytypes import AgentID, OperatingSystem

from .i_agent_command_builder import IAgentCommandBuilder
from .linux_agent_command_builder import LinuxAgentCommandBuilder
from .windows_agent_command_builder import WindowsAgentCommandBuilder


class IAgentCommandBuilderFactory(ABC):
    @abstractmethod
    def create_agent_command_builder(
        self, target_host: TargetHost, servers: list[str], current_depth: int = 0
    ) -> IAgentCommandBuilder:
        """
        Builds an IAgentCommandBuilder that construct the Agent command
        """


class AgentCommandBuilderFactory(IAgentCommandBuilderFactory):
    def __init__(
        self,
        agent_id: AgentID,
        otp_provider: IAgentOTPProvider,
        agent_otp_environment_variable: str,
    ):
        self._agent_id = agent_id
        self._otp_provider = otp_provider
        self._agent_otp_environment_variable = agent_otp_environment_variable

    def create_agent_command_builder(
        self, target_host: TargetHost, servers: list[str], current_depth: int = 0
    ) -> IAgentCommandBuilder:
        if target_host.operating_system == OperatingSystem.WINDOWS:
            return WindowsAgentCommandBuilder(
                self._agent_id,
                servers,
                self._otp_provider,
                self._agent_otp_environment_variable,
                current_depth,
            )
        if target_host.operating_system == OperatingSystem.LINUX:
            return LinuxAgentCommandBuilder(
                self._agent_id,
                servers,
                self._otp_provider,
                self._agent_otp_environment_variable,
                current_depth,
            )
        raise ValueError("Unsupported OS for build Agent Commands")
