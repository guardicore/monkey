import logging
import os
from typing import Dict, Iterable

from common.common_consts.post_breach_consts import POST_BREACH_FILE_EXECUTION
from common.utils.attack_utils import ScanStatus
from infection_monkey.control import ControlClient
from infection_monkey.i_puppet import PostBreachData
from infection_monkey.network.tools import get_interface_to_target
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.attack.t1105_telem import T1105Telem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.monkey_dir import get_monkey_dir_path

logger = logging.getLogger(__name__)


DIR_CHANGE_WINDOWS = "cd %s & "
DIR_CHANGE_LINUX = "cd %s ; "


class CustomPBA(PBA):
    """
    Defines user's configured post breach action.
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger, control_client: ControlClient):
        super(CustomPBA, self).__init__(
            telemetry_messenger, POST_BREACH_FILE_EXECUTION, timeout=None
        )
        self.filename = ""
        self.control_client = control_client

    def run(self, options: Dict) -> Iterable[PostBreachData]:
        self._set_options(options)
        return super().run(options)

    def _set_options(self, options: Dict):
        if is_windows_os():
            # Add windows commands to PBA's
            if options["windows_filename"]:
                self.filename = options["windows_filename"]
                if options["windows_command"]:
                    # Add change dir command, because user will try to access his file
                    self.command = (DIR_CHANGE_WINDOWS % get_monkey_dir_path()) + options[
                        "windows_command"
                    ]
            elif options["windows_command"]:
                self.command = options["windows_command"]
        else:
            # Add linux commands to PBA's
            if options["linux_filename"]:
                self.filename = options["linux_filename"]
                if options["linux_command"]:
                    # Add change dir command, because user will try to access his file
                    self.command = (DIR_CHANGE_LINUX % get_monkey_dir_path()) + options[
                        "linux_command"
                    ]
            elif options["linux_command"]:
                self.command = options["linux_command"]

    def _execute_default(self):
        if self.filename:
            self.download_pba_file(get_monkey_dir_path(), self.filename)
        return super(CustomPBA, self)._execute_default()

    def download_pba_file(self, dst_dir, filename):
        """
        Handles post breach action file download
        :param dst_dir: Destination directory
        :param filename: Filename
        :return: True if successful, false otherwise
        """

        pba_file_contents = self.control_client.get_pba_file(filename)

        status = None
        if not pba_file_contents:
            logger.error("Island didn't respond with post breach file.")
            status = ScanStatus.SCANNED

        if not status:
            status = ScanStatus.USED

        self.telemetry_messenger.send_telemetry(
            T1105Telem(
                status,
                self.control_client.server_address.split(":")[0],
                get_interface_to_target(self.control_client.server_address.split(":")[0]),
                filename,
            )
        )

        if status == ScanStatus.SCANNED:
            return False

        try:
            with open(os.path.join(dst_dir, filename), "wb") as written_PBA_file:
                written_PBA_file.write(pba_file_contents)
            return True
        except IOError as e:
            logger.error("Can not upload post breach file to target machine: %s" % e)
            return False
