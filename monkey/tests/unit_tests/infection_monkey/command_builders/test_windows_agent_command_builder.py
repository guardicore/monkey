from pathlib import PureWindowsPath

import pytest
from agentpluginapi import (
    DropperExecutionMode,
    IAgentCommandBuilderFactory,
    IWindowsAgentCommandBuilder,
    WindowsDownloadMethod,
    WindowsDownloadOptions,
    WindowsRunOptions,
    WindowsShell,
)
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG

AGENT_DESTINATION_PATH = PureWindowsPath("C:\\Windows\\Temp\\agent.exe")
DROPPER_DESTINATION_PATH = PureWindowsPath("C:\\Temp\\dropper.exe")
EXPECTED_AGENT_DESTINATION_PATH = str(AGENT_DESTINATION_PATH)
EXPECTED_DROPPER_DESTINATION_PATH = str(DROPPER_DESTINATION_PATH)
DOWNLOAD_URL = "http://127.0.0.1/agent"


@pytest.fixture
def windows_agent_command_builder(
    agent_command_builder_factory: IAgentCommandBuilderFactory,
) -> IWindowsAgentCommandBuilder:
    return agent_command_builder_factory.create_windows_agent_command_builder()


def test_initial_command(windows_agent_command_builder: IWindowsAgentCommandBuilder):
    assert windows_agent_command_builder.get_command() == ""


@pytest.mark.parametrize(
    "expected_method, not_expected_method, download_method",
    [
        ("Invoke-WebRequest", "System.Net.WebClient", WindowsDownloadMethod.WEB_REQUEST),
        ("System.Net.WebClient", "Invoke-WebRequest", WindowsDownloadMethod.WEB_CLIENT),
    ],
)
def test_build_download_command(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    expected_method: str,
    not_expected_method: str,
    download_method: WindowsDownloadMethod,
):
    windows_download_options = WindowsDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=download_method,
        download_url=DOWNLOAD_URL,
    )

    windows_agent_command_builder.build_download_command(windows_download_options)
    actual_command = windows_agent_command_builder.get_command()

    assert expected_method in actual_command
    assert not_expected_method not in actual_command
    assert DOWNLOAD_URL in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command


@pytest.mark.parametrize(
    "shell, expected_otp_set",
    [
        (WindowsShell.CMD, "set"),
        (WindowsShell.POWERSHELL, "$env"),
    ],
)
def test_build_run_command_none(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    shell: WindowsShell,
    expected_otp_set: str,
    otp: str,
    agent_otp_environment_variable: str,
    agent_id: AgentID,
):
    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.NONE,
        shell=shell,
    )

    windows_agent_command_builder.build_run_command(windows_run_options)
    actual_command = windows_agent_command_builder.get_command()

    assert expected_otp_set in actual_command
    assert agent_otp_environment_variable in actual_command
    assert otp in actual_command
    assert str(agent_id) in actual_command
    assert MONKEY_ARG in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command


@pytest.mark.parametrize(
    "shell, expected_otp_set",
    [
        (WindowsShell.CMD, "set"),
        (WindowsShell.POWERSHELL, "$env"),
    ],
)
def test_build_run_command_dropper(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    shell: WindowsShell,
    expected_otp_set: str,
    otp: str,
    agent_otp_environment_variable: str,
    agent_id: AgentID,
):
    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.DROPPER,
        shell=shell,
        dropper_destination_path=DROPPER_DESTINATION_PATH,
    )

    windows_agent_command_builder.build_run_command(windows_run_options)
    actual_command = windows_agent_command_builder.get_command()

    assert expected_otp_set in actual_command
    assert agent_otp_environment_variable in actual_command
    assert otp in actual_command
    assert str(agent_id) in actual_command
    assert DROPPER_ARG in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command
    assert EXPECTED_DROPPER_DESTINATION_PATH in actual_command


@pytest.mark.parametrize(
    "shell, expected_otp_set",
    [
        (WindowsShell.CMD, "set"),
        (WindowsShell.POWERSHELL, "$env"),
    ],
)
def test_build_run_command_script(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    shell: WindowsShell,
    expected_otp_set: str,
    otp: str,
    agent_otp_environment_variable: str,
    agent_id: AgentID,
):
    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.SCRIPT,
        shell=shell,
    )

    windows_agent_command_builder.build_run_command(windows_run_options)
    actual_command = windows_agent_command_builder.get_command()

    assert expected_otp_set in actual_command
    assert agent_otp_environment_variable in actual_command
    assert otp in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command
    assert str(agent_id) not in actual_command
    assert DROPPER_ARG not in actual_command
    assert MONKEY_ARG not in actual_command


def test_build_run_command_unempty_download(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
):
    windows_download_options = WindowsDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=WindowsDownloadMethod.WEB_REQUEST,
        download_url=DOWNLOAD_URL,
    )
    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.DROPPER,
        shell=WindowsShell.CMD,
        dropper_destination_path=DROPPER_DESTINATION_PATH,
    )

    windows_agent_command_builder.build_download_command(windows_download_options)
    windows_agent_command_builder.build_run_command(windows_run_options)
    actual_command = windows_agent_command_builder.get_command()

    assert "powershell" in actual_command
    assert "Invoke-WebRequest" in actual_command
    assert "cmd.exe /c" in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command
    assert DROPPER_ARG in actual_command


def test_command_reset(windows_agent_command_builder: IWindowsAgentCommandBuilder):
    windows_download_options = WindowsDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=WindowsDownloadMethod.WEB_REQUEST,
        download_url=DOWNLOAD_URL,
    )

    windows_agent_command_builder.build_download_command(windows_download_options)
    assert len(windows_agent_command_builder.get_command()) > 0

    windows_agent_command_builder.reset_command()
    assert windows_agent_command_builder.get_command() == ""
