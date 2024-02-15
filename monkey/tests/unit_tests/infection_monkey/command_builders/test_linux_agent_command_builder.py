from pathlib import PurePosixPath

import pytest
from agentpluginapi import (
    DropperExecutionMode,
    IAgentCommandBuilderFactory,
    ILinuxAgentCommandBuilder,
    LinuxDownloadMethod,
    LinuxDownloadOptions,
    LinuxRunOptions,
)
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG

AGENT_DESTINATION_PATH = PurePosixPath("/tmp/agent")
DROPPER_DESTINATION_PATH = PurePosixPath("/tmp/dropper")
EXPECTED_AGENT_DESTINATION_PATH = str(AGENT_DESTINATION_PATH)
EXPECTED_DROPPER_DESTINATION_PATH = str(DROPPER_DESTINATION_PATH)
DOWNLOAD_URL = "http://127.0.0.1/agent"


@pytest.fixture
def linux_agent_command_builder(
    agent_command_builder_factory: IAgentCommandBuilderFactory,
) -> ILinuxAgentCommandBuilder:
    return agent_command_builder_factory.create_linux_agent_command_builder()


def test_initial_command(linux_agent_command_builder: ILinuxAgentCommandBuilder):
    assert linux_agent_command_builder.get_command() == ""


@pytest.mark.parametrize(
    "expected_method, not_expected_method, download_method",
    [
        ("wget", "curl", LinuxDownloadMethod.WGET),
        ("curl", "wget", LinuxDownloadMethod.CURL),
    ],
)
def test_build_download_command(
    linux_agent_command_builder: ILinuxAgentCommandBuilder,
    expected_method: str,
    not_expected_method: str,
    download_method: LinuxDownloadMethod,
):
    linux_download_options = LinuxDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=download_method,
        download_url=DOWNLOAD_URL,
    )

    linux_agent_command_builder.build_download_command(linux_download_options)
    actual_command = linux_agent_command_builder.get_command()

    assert expected_method in actual_command
    assert not_expected_method not in actual_command
    assert "chmod" in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command


def test_build_run_command_none(
    linux_agent_command_builder: ILinuxAgentCommandBuilder,
    agent_otp_environment_variable: str,
    otp: str,
    agent_id: AgentID,
):
    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.NONE,
    )

    linux_agent_command_builder.build_run_command(linux_run_options)
    actual_command = linux_agent_command_builder.get_command()

    assert agent_otp_environment_variable in actual_command
    assert otp in actual_command
    assert str(agent_id) in actual_command
    assert MONKEY_ARG in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command


def test_build_run_command_dropper(
    linux_agent_command_builder: ILinuxAgentCommandBuilder,
    agent_otp_environment_variable: str,
    otp: str,
    agent_id: AgentID,
):
    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.DROPPER,
        dropper_destination_path=DROPPER_DESTINATION_PATH,
    )

    linux_agent_command_builder.build_run_command(linux_run_options)
    actual_command = linux_agent_command_builder.get_command()

    assert agent_otp_environment_variable in actual_command
    assert otp in actual_command
    assert str(agent_id) in actual_command
    assert DROPPER_ARG in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command
    assert EXPECTED_DROPPER_DESTINATION_PATH in actual_command


def test_build_run_command_script(
    linux_agent_command_builder: ILinuxAgentCommandBuilder,
    agent_otp_environment_variable: str,
    otp: str,
    agent_id: AgentID,
):
    linux_run_options = LinuxRunOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        dropper_execution_mode=DropperExecutionMode.SCRIPT,
    )

    linux_agent_command_builder.build_run_command(linux_run_options)
    actual_command = linux_agent_command_builder.get_command()

    assert agent_otp_environment_variable in actual_command
    assert otp in actual_command
    assert EXPECTED_AGENT_DESTINATION_PATH in actual_command
    assert str(agent_id) not in actual_command
    assert DROPPER_ARG not in actual_command
    assert MONKEY_ARG not in actual_command


def test_command_reset(linux_agent_command_builder: ILinuxAgentCommandBuilder):
    linux_download_options = LinuxDownloadOptions(
        agent_destination_path=AGENT_DESTINATION_PATH,
        download_method=LinuxDownloadMethod.WGET,
        download_url=DOWNLOAD_URL,
    )

    linux_agent_command_builder.build_download_command(linux_download_options)
    assert len(linux_agent_command_builder.get_command()) > 0

    linux_agent_command_builder.reset_command()
    assert linux_agent_command_builder.get_command() == ""
