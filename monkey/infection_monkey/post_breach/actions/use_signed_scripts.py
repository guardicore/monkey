import logging
import subprocess
from typing import Dict

from common.common_consts.post_breach_consts import POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC
from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT, SHORT_REQUEST_TIMEOUT
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.signed_script_proxy.signed_script_proxy import (
    cleanup_changes,
    copy_executable_to_cwd,
    get_commands_to_proxy_execution_using_signed_script,
)
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)


class SignedScriptProxyExecution(PBA):
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        windows_cmds = get_commands_to_proxy_execution_using_signed_script()
        super().__init__(
            telemetry_messenger,
            POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC,
            windows_cmd=" ".join(windows_cmds),
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )

    def run(self, options: Dict):
        original_comspec = ""
        try:
            if is_windows_os():
                copy_executable_to_cwd()
                original_comspec = subprocess.check_output(  # noqa: DUO116
                    "if defined COMSPEC echo %COMSPEC%", shell=True, timeout=SHORT_REQUEST_TIMEOUT
                ).decode()
            super().run(options)
            return self.pba_data
        except Exception as e:
            logger.warning(
                f"An exception occurred on running PBA "
                f"{POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC}: {str(e)}"
            )
        finally:
            cleanup_changes(original_comspec)
