import logging
import time

import botocore

from common.utils import Timer

REMOTE_COMMAND_TIMEOUT = 5
STATUS_CHECK_SLEEP_TIME = 1
LINUX_DOCUMENT_NAME = "AWS-RunShellScript"
WINDOWS_DOCUMENT_NAME = "AWS-RunPowerShellScript"

logger = logging.getLogger(__name__)


# TODO: Make sure the return type is compatible with what RemoteRun is expecting. Add typehint.
def start_infection_monkey_agent(
    aws_client: botocore.client.BaseClient, target_instance_id: str, target_os: str, island_ip: str
):
    """
    Run a command on a remote AWS instance
    """
    command = _get_run_agent_command(target_os, island_ip)
    command_id = _run_command_async(aws_client, target_instance_id, target_os, command)
    _wait_for_command_to_complete(aws_client, target_instance_id, command_id)

    # TODO: Return result


def _get_run_agent_command(target_os: str, island_ip: str):
    if target_os == "linux":
        return _get_run_monkey_cmd_linux_line(island_ip)

    return _get_run_monkey_cmd_windows_line(island_ip)


def _get_run_monkey_cmd_linux_line(island_ip):
    binary_name = "monkey-linux-64"

    download_url = f"https://{island_ip}:5000/api/agent/download/linux"
    download_cmd = f"wget --no-check-certificate {download_url} -O {binary_name}"

    chmod_cmd = f"chmod +x {binary_name}"
    run_agent_cmd = f"./{binary_name} m0nk3y -s {island_ip}:5000"

    return f"{download_cmd}; {chmod_cmd}; {run_agent_cmd}"


def _get_run_monkey_cmd_windows_line(island_ip):
    agent_exe_path = r".\\monkey.exe"

    ignore_ssl_errors_cmd = (
        "[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}"
    )

    download_url = f"https://{island_ip}:5000/api/agent/download/windows"
    download_cmd = (
        f"(New-Object System.Net.WebClient).DownloadFile('{download_url}', '{agent_exe_path}')"
    )

    run_agent_cmd = (
        f"Start-Process -FilePath '{agent_exe_path}' -ArgumentList 'm0nk3y -s {island_ip}:5000'"
    )

    return f"{ignore_ssl_errors_cmd}; {download_cmd}; {run_agent_cmd};"


def _run_command_async(
    aws_client: botocore.client.BaseClient, target_instance_id: str, target_os: str, command: str
):
    doc_name = LINUX_DOCUMENT_NAME if target_os == "linux" else WINDOWS_DOCUMENT_NAME

    logger.debug(f'Running command on {target_instance_id} -- {doc_name}: "{command}"')
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
    aws_client: botocore.client.BaseClient, target_instance_id: str, command_id: str
):
    timer = Timer()
    timer.set(REMOTE_COMMAND_TIMEOUT)

    while not timer.is_expired():
        time.sleep(STATUS_CHECK_SLEEP_TIME)

        command_status = aws_client.get_command_invocation(
            CommandId=command_id, InstanceId=target_instance_id
        )["Status"]
        logger.debug(f"Command {command_id} status: {command_status}")

        if command_status == "Success":
            break

        if command_status != "InProgress":
            # TODO: Create an exception for this occasion and raise it with useful information.
            raise Exception("COMMAND FAILED")
