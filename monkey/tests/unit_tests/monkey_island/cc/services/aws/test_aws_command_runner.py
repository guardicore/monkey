from itertools import chain, repeat
from unittest.mock import MagicMock

import pytest
from monkeytypes import OTP

from monkey_island.cc.services.aws.aws_command_runner import (
    LINUX_DOCUMENT_NAME,
    WINDOWS_DOCUMENT_NAME,
    AWSCommandResults,
    AWSCommandStatus,
    start_infection_monkey_agent,
)

TIMEOUT = 0.1
INSTANCE_ID = "BEEFFACE"
ISLAND_IP = "127.0.0.1"
INSTANCE_OTP = OTP("supersecretone")


@pytest.fixture
def send_command_response():
    return {
        "Command": {
            "CloudWatchOutputConfig": {
                "CloudWatchLogGroupName": "",
                "CloudWatchOutputEnabled": False,
            },
            "CommandId": "fe3cf24f-71b7-42b9-93ca-e27c34dd0581",
            "CompletedCount": 0,
            "DocumentName": "AWS-RunShellScript",
            "DocumentVersion": "$DEFAULT",
            "InstanceIds": ["i-0b62d6f0b0d9d7e77"],
            "OutputS3Region": "eu-central-1",
            "Parameters": {"commands": []},
            "Status": "Pending",
            "StatusDetails": "Pending",
            "TargetCount": 1,
            "Targets": [],
            "TimeoutSeconds": 3600,
        },
        "ResponseMetadata": {
            "HTTPHeaders": {
                "connection": "keep-alive",
                "content-length": "973",
                "content-type": "application/x-amz-json-1.1",
                "date": "Tue, 10 May 2022 12:35:49 GMT",
                "server": "Server",
                "x-amzn-requestid": "110b1563-aaf0-4e09-bd23-2db465822be7",
            },
            "HTTPStatusCode": 200,
            "RequestId": "110b1563-aaf0-4e09-bd23-2db465822be7",
            "RetryAttempts": 0,
        },
    }


@pytest.fixture
def in_progress_response():
    return {
        "CloudWatchOutputConfig": {"CloudWatchLogGroupName": "", "CloudWatchOutputEnabled": False},
        "CommandId": "a5332cc6-0f9f-48e6-826a-d4bd7cabc2ee",
        "Comment": "",
        "DocumentName": "AWS-RunShellScript",
        "DocumentVersion": "$DEFAULT",
        "ExecutionEndDateTime": "",
        "InstanceId": "i-0b62d6f0b0d9d7e77",
        "PluginName": "aws:runShellScript",
        "ResponseCode": -1,
        "StandardErrorContent": "",
        "StandardErrorUrl": "",
        "StandardOutputContent": "",
        "StandardOutputUrl": "",
        "Status": "InProgress",
        "StatusDetails": "InProgress",
    }


@pytest.fixture
def success_response():
    return {
        "CloudWatchOutputConfig": {"CloudWatchLogGroupName": "", "CloudWatchOutputEnabled": False},
        "CommandId": "a5332cc6-0f9f-48e6-826a-d4bd7cabc2ee",
        "Comment": "",
        "DocumentName": "AWS-RunShellScript",
        "DocumentVersion": "$DEFAULT",
        "ExecutionEndDateTime": "",
        "InstanceId": "i-0b62d6f0b0d9d7e77",
        "PluginName": "aws:runShellScript",
        "ResponseCode": -1,
        "StandardErrorContent": "",
        "StandardErrorUrl": "",
        "StandardOutputContent": "",
        "StandardOutputUrl": "",
        "Status": "Success",
        "StatusDetails": "Success",
    }


@pytest.fixture
def error_response():
    return {
        "CloudWatchOutputConfig": {"CloudWatchLogGroupName": "", "CloudWatchOutputEnabled": False},
        "CommandId": "a5332cc6-0f9f-48e6-826a-d4bd7cabc2ee",
        "Comment": "",
        "DocumentName": "AWS-RunShellScript",
        "DocumentVersion": "$DEFAULT",
        "ExecutionEndDateTime": "",
        "InstanceId": "i-0b62d6f0b0d9d7e77",
        "PluginName": "aws:runShellScript",
        "ResponseCode": -1,
        "StandardErrorContent": "ERROR RUNNING COMMAND",
        "StandardErrorUrl": "",
        "StandardOutputContent": "",
        "StandardOutputUrl": "",
        # NOTE: "Error" is technically not a valid value for this field, but we want to test that
        #       anything other than "Success" and "InProgress" is treated as an error. This is
        #       simpler than testing all of the different possible error cases.
        "Status": "Error",
        "StatusDetails": "Error",
    }


@pytest.fixture(autouse=True)
def patch_timeouts(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.services.aws.aws_command_runner.STATUS_CHECK_SLEEP_TIME", 0.01
    )


@pytest.fixture
def successful_mock_client(send_command_response, success_response):
    aws_client = MagicMock()
    aws_client.send_command = MagicMock(return_value=send_command_response)
    aws_client.get_command_invocation = MagicMock(return_value=success_response)

    return aws_client


def test_correct_instance_id(successful_mock_client):
    start_infection_monkey_agent(
        successful_mock_client, INSTANCE_ID, "linux", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )

    successful_mock_client.send_command.assert_called_once()
    call_args_kwargs = successful_mock_client.send_command.call_args[1]
    assert call_args_kwargs["InstanceIds"] == [INSTANCE_ID]


def test_linux_doc_name(successful_mock_client):
    start_infection_monkey_agent(
        successful_mock_client, INSTANCE_ID, "linux", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )

    successful_mock_client.send_command.assert_called_once()
    call_args_kwargs = successful_mock_client.send_command.call_args[1]
    assert call_args_kwargs["DocumentName"] == LINUX_DOCUMENT_NAME


def test_windows_doc_name(successful_mock_client):
    start_infection_monkey_agent(
        successful_mock_client, INSTANCE_ID, "windows", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )

    successful_mock_client.send_command.assert_called_once()
    call_args_kwargs = successful_mock_client.send_command.call_args[1]
    assert call_args_kwargs["DocumentName"] == WINDOWS_DOCUMENT_NAME


def test_linux_command(successful_mock_client):
    start_infection_monkey_agent(
        successful_mock_client, INSTANCE_ID, "linux", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )

    successful_mock_client.send_command.assert_called_once()
    call_args_kwargs = successful_mock_client.send_command.call_args[1]
    assert "wget" in call_args_kwargs["Parameters"]["commands"][0]


def test_windows_command(successful_mock_client):
    start_infection_monkey_agent(
        successful_mock_client, INSTANCE_ID, "windows", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )

    successful_mock_client.send_command.assert_called_once()
    call_args_kwargs = successful_mock_client.send_command.call_args[1]
    assert "DownloadFile" in call_args_kwargs["Parameters"]["commands"][0]


def test_multiple_status_queries(send_command_response, in_progress_response, success_response):
    aws_client = MagicMock()
    aws_client.send_command = MagicMock(return_value=send_command_response)
    aws_client.get_command_invocation = MagicMock(
        side_effect=chain([in_progress_response, in_progress_response], repeat(success_response))
    )

    command_results = start_infection_monkey_agent(
        aws_client, INSTANCE_ID, "windows", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )
    assert command_results.status == AWSCommandStatus.SUCCESS


def test_in_progress_timeout(send_command_response, in_progress_response):
    aws_client = MagicMock()
    aws_client.send_command = MagicMock(return_value=send_command_response)
    aws_client.get_command_invocation = MagicMock(return_value=in_progress_response)

    command_results = start_infection_monkey_agent(
        aws_client, INSTANCE_ID, "windows", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )
    assert command_results.status == AWSCommandStatus.IN_PROGRESS


def test_failed_command(send_command_response, error_response):
    aws_client = MagicMock()
    aws_client.send_command = MagicMock(return_value=send_command_response)
    aws_client.get_command_invocation = MagicMock(return_value=error_response)

    command_results = start_infection_monkey_agent(
        aws_client, INSTANCE_ID, "windows", INSTANCE_OTP, ISLAND_IP, TIMEOUT
    )
    assert command_results.status == AWSCommandStatus.ERROR


@pytest.mark.parametrize(
    "status, success",
    [
        (AWSCommandStatus.SUCCESS, True),
        (AWSCommandStatus.IN_PROGRESS, False),
        (AWSCommandStatus.ERROR, False),
    ],
)
def test_command_resuls_status(status, success):
    results = AWSCommandResults(INSTANCE_ID, 0, "", "", status)
    assert results.success == success
