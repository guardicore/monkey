from typing import Sequence

from agentpluginapi import (
    IAgentCommandBuilderFactory,
    IAgentOTPProvider,
    ILinuxAgentCommandBuilder,
    IWindowsAgentCommandBuilder,
)
from monkeytypes import AgentID

from .linux_agent_command_builder import LinuxAgentCommandBuilder


class AgentCommandBuilderFactory(IAgentCommandBuilderFactory):
    def __init__(
        self,
        agent_id: AgentID,
        servers: Sequence[str],
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
        pass
