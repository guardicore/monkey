import logging
import subprocess
from typing import Dict, Iterable, List, Optional, Tuple

from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT
from common.utils.attack_utils import ScanStatus
from infection_monkey.i_puppet.i_puppet import PostBreachData
from infection_monkey.telemetry.attack.t1064_telem import T1064Telem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)


class PBA:
    """
    Post breach action object. Can be extended to support more than command execution on target
    machine.
    """

    def __init__(
        self,
        telemetry_messenger: ITelemetryMessenger,
        name="unknown",
        linux_cmd="",
        windows_cmd="",
        timeout: Optional[float] = LONG_REQUEST_TIMEOUT,
    ):
        """
        :param name: Name of post breach action.
        :param linux_cmd: Command that will be executed on breached machine
        :param windows_cmd: Command that will be executed on breached machine
        """
        self.command = PBA.choose_command(linux_cmd, windows_cmd)
        self.name = name
        self.pba_data: List[PostBreachData] = []
        self.telemetry_messenger = telemetry_messenger
        self.timeout = timeout

    def run(self, options: Dict) -> Iterable[PostBreachData]:
        """
        Runs post breach action command
        """
        if self.command:
            exec_funct = self._execute_default
            result = exec_funct()
            if self.scripts_were_used_successfully(result):
                self.telemetry_messenger.send_telemetry(
                    T1064Telem(
                        ScanStatus.USED,
                        f"Scripts were used to execute {self.name} post breach action.",
                    )
                )
            self.pba_data.append(PostBreachData(self.name, self.command, result))
        else:
            logger.debug(f"No command available for PBA '{self.name}' on current OS, skipping.")

        return self.pba_data

    def is_script(self):
        """
        Determines if PBA is a script (PBA might be a single command)
        :return: True if PBA is a script(series of OS commands)
        """
        return isinstance(self.command, list) and len(self.command) > 1

    def scripts_were_used_successfully(self, pba_execution_result):
        """
        Determines if scripts were used to execute PBA and if they succeeded
        :param pba_execution_result: result of execution function. e.g. self._execute_default
        :return: True if scripts were used, False otherwise
        """
        pba_execution_succeeded = pba_execution_result[1]
        return pba_execution_succeeded and self.is_script()

    def _execute_default(self) -> Tuple[str, bool]:
        """
        Default post breach command execution routine
        :return: Tuple of command's output string and boolean, indicating if it succeeded
        """
        try:
            output = subprocess.check_output(  # noqa: DUO116
                self.command, stderr=subprocess.STDOUT, shell=True, timeout=self.timeout
            ).decode()
            return output, True
        except subprocess.CalledProcessError as err:
            return bytes(err.output).decode(), False
        except subprocess.TimeoutExpired as err:
            return str(err), False

    @staticmethod
    def choose_command(linux_cmd, windows_cmd):
        """
        Helper method that chooses between linux and windows commands.
        :param linux_cmd:
        :param windows_cmd:
        :return: Command for current os
        """
        return windows_cmd if is_windows_os() else linux_cmd
