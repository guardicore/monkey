import logging
import time
from dataclasses import dataclass
from enum import Enum, auto

import botocore
from egg_timer import EggTimer
from monkeytypes import OTP

from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE

STATUS_CHECK_SLEEP_TIME = 1
LINUX_DOCUMENT_NAME = "AWS-RunShellScript"
WINDOWS_DOCUMENT_NAME = "AWS-RunPowerShellScript"

# Setting the log level of botocore to CRITICAL so that
# it doesn't log out the commands sent to the AWS instance,
# thus hiding the Agent's OTP
logging.getLogger("botocore").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class AWSCommandStatus(Enum):
    SUCCESS = auto()
    IN_PROGRESS = auto()
    ERROR = auto()


@dataclass(frozen=True)
class AWSCommandResults:
    instance_id: str
    response_code: int
    stdout: str
    stderr: str
    status: AWSCommandStatus

    @property
    def success(self):
        return self.status == AWSCommandStatus.SUCCESS


def start_infection_monkey_agent(
    aws_client: botocore.client.BaseClient,
    target_instance_id: str,
    target_os: str,
    otp: OTP,
    island_ip: str,
    timeout: float,
) -> AWSCommandResults:
    """
    Run a command on a remote AWS instance
    """
    command = _get_run_agent_command(target_os, island_ip, otp)
    command_id = _run_command_async(aws_client, target_instance_id, target_os, command)

    _wait_for_command_to_complete(aws_client, target_instance_id, command_id, timeout)
    return _fetch_command_results(aws_client, target_instance_id, command_id)


def _get_run_agent_command(target_os: str, island_ip: str, otp: OTP):
    if target_os == "linux":
        return _get_run_monkey_cmd_linux_line(island_ip, otp)

    return _get_run_monkey_cmd_windows_line(island_ip, otp)


def _get_run_monkey_cmd_linux_line(island_ip: str, otp: OTP):
    binary_name = "monkey-linux-64"

    download_url = f"https://{island_ip}:5000/api/agent-binaries/linux"
    download_cmd = f"wget --no-check-certificate {download_url} -O {binary_name}"

    chmod_cmd = f"chmod +x {binary_name}"
    run_agent_cmd = (
        f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={otp.get_secret_value()} "
        f"./{binary_name} m0nk3y -s {island_ip}:5000"
    )
    return f"{download_cmd}; {chmod_cmd}; {run_agent_cmd}"


def _get_run_monkey_cmd_windows_line(island_ip: str, otp: OTP):
    agent_exe_path = r".\\monkey.exe"

    ignore_ssl_errors_cmd = (
        "[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}"
    )

    download_url = f"https://{island_ip}:5000/api/agent-binaries/windows"
    download_cmd = (
        f"(New-Object System.Net.WebClient).DownloadFile('{download_url}', '{agent_exe_path}')"
    )
    set_otp = f"$env:{AGENT_OTP_ENVIRONMENT_VARIABLE}='{otp.get_secret_value()}'"
    run_agent_cmd = (
        f"Start-Process -FilePath '{agent_exe_path}' -ArgumentList 'm0nk3y -s {island_ip}:5000'"
    )

    return f"{ignore_ssl_errors_cmd}; {download_cmd}; {set_otp}; {run_agent_cmd};"


def _run_command_async(
    aws_client: botocore.client.BaseClient, target_instance_id: str, target_os: str, command: str
):
    doc_name = LINUX_DOCUMENT_NAME if target_os == "linux" else WINDOWS_DOCUMENT_NAME

    logger.debug(f"Running command on {target_instance_id} -- {doc_name}")
    command_response = aws_client.send_command(
        DocumentName=doc_name,
        Parameters={"commands": [command]},
        InstanceIds=[target_instance_id],
    )

    command_id = command_response["Command"]["CommandId"]
    logger.debug(
        f"Started command on AWS instance {target_instance_id} with command ID {command_id}"
    )

    return command_id


def _wait_for_command_to_complete(
    aws_client: botocore.client.BaseClient, target_instance_id: str, command_id: str, timeout: float
):
    timer = EggTimer()
    timer.set(timeout)

    while not timer.is_expired():
        time.sleep(STATUS_CHECK_SLEEP_TIME)

        command_results = _fetch_command_results(aws_client, target_instance_id, command_id)
        logger.debug(f"Command {command_id} status: {command_results.status.name}")

        if command_results.status != AWSCommandStatus.IN_PROGRESS:
            return


def _fetch_command_results(
    aws_client: botocore.client.BaseClient, target_instance_id: str, command_id: str
) -> AWSCommandResults:
    command_results = aws_client.get_command_invocation(
        CommandId=command_id, InstanceId=target_instance_id
    )
    command_status = command_results["Status"]
    logger.debug(f"Command {command_id} status: {command_status}")

    if command_status == "Success":
        aws_command_result_status = AWSCommandStatus.SUCCESS
    elif command_status == "InProgress":
        aws_command_result_status = AWSCommandStatus.IN_PROGRESS
    else:
        aws_command_result_status = AWSCommandStatus.ERROR

    return AWSCommandResults(
        target_instance_id,
        command_results["ResponseCode"],
        command_results["StandardOutputContent"],
        command_results["StandardErrorContent"],
        aws_command_result_status,
    )
