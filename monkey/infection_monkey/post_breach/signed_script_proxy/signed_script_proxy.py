import logging
import subprocess
from pathlib import Path
from shutil import copyfile

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from infection_monkey.post_breach.signed_script_proxy.windows.signed_script_proxy import (
    get_windows_commands_to_delete_temp_comspec,
    get_windows_commands_to_proxy_execution_using_signed_script,
    get_windows_commands_to_reset_comspec,
)
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)

EXECUTABLE_NAME = "T1216_random_executable.exe"
EXECUTABLE_SRC_PATH = Path(__file__).parent / EXECUTABLE_NAME
TEMP_COMSPEC = Path.cwd() / "T1216_random_executable.exe"


def get_commands_to_proxy_execution_using_signed_script():
    windows_cmds = get_windows_commands_to_proxy_execution_using_signed_script(TEMP_COMSPEC)
    return windows_cmds


def copy_executable_to_cwd():
    logger.debug(f"Copying executable from {EXECUTABLE_SRC_PATH} to {TEMP_COMSPEC}")
    copyfile(EXECUTABLE_SRC_PATH, TEMP_COMSPEC)


def cleanup_changes(original_comspec):
    if is_windows_os():
        try:
            subprocess.run(  # noqa: DUO116
                get_windows_commands_to_reset_comspec(original_comspec),
                shell=True,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            subprocess.run(  # noqa: DUO116
                get_windows_commands_to_delete_temp_comspec(TEMP_COMSPEC),
                shell=True,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
        except subprocess.CalledProcessError as err:
            logger.error(err.output.decode())
        except subprocess.TimeoutExpired as err:
            logger.error(str(err))
