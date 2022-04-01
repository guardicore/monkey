import logging
import subprocess
from pathlib import Path

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from infection_monkey.utils.environment import is_windows_os

MODIFY_POWERSHELL_STARTUP_SCRIPT = Path(__file__).parent / "modify_powershell_startup_file.ps1"

logger = logging.getLogger(__name__)


def get_windows_commands_to_modify_shell_startup_files():
    if not is_windows_os():
        return "", []

    # get powershell startup file path
    shell_startup_file = subprocess.check_output("powershell $Profile").decode().split("\r\n")[0]
    shell_startup_file_path_components = shell_startup_file.split("\\")

    # get list of usernames
    command = "dir C:\\Users /b"
    try:
        users = (
            subprocess.check_output(  # noqa: DUO116
                command, shell=True, timeout=MEDIUM_REQUEST_TIMEOUT
            )
            .decode()
            .split("\r\n")[:-1]
        )
        users.remove("Public")
    except subprocess.TimeoutExpired:
        logger.error(f"Command {command} timed out")
        return "", []

    startup_files_per_user = [
        "\\".join(
            shell_startup_file_path_components[:2] + [user] + shell_startup_file_path_components[3:]
        )
        for user in users
    ]

    return [
        "powershell.exe",
        str(MODIFY_POWERSHELL_STARTUP_SCRIPT),
        "-startup_file_path {0}",
    ], startup_files_per_user
