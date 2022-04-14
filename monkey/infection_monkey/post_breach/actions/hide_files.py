from typing import Dict

from common.common_consts.post_breach_consts import POST_BREACH_HIDDEN_FILES
from infection_monkey.i_puppet.i_puppet import PostBreachData
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.hidden_files import (
    cleanup_hidden_files,
    get_commands_to_hide_files,
    get_commands_to_hide_folders,
)
from infection_monkey.utils.windows.hidden_files import get_winAPI_to_hide_files

HIDDEN_FSO_CREATION_COMMANDS = [get_commands_to_hide_files, get_commands_to_hide_folders]


class HiddenFiles(PBA):
    """
    This PBA attempts to create hidden files and folders.
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        super(HiddenFiles, self).__init__(telemetry_messenger, name=POST_BREACH_HIDDEN_FILES)

    def run(self, options: Dict):
        # create hidden files and folders
        for function_to_get_commands in HIDDEN_FSO_CREATION_COMMANDS:
            linux_cmds, windows_cmds = function_to_get_commands()
            super(HiddenFiles, self).__init__(
                self.telemetry_messenger,
                name=POST_BREACH_HIDDEN_FILES,
                linux_cmd=" ".join(linux_cmds),
                windows_cmd=windows_cmds,
            )
            super(HiddenFiles, self).run(options)

        if is_windows_os():  # use winAPI
            result, status = get_winAPI_to_hide_files()
            # no command here, used WinAPI
            self.pba_data.append(PostBreachData(self.name, self.command, (result, status)))

        # cleanup hidden files and folders
        cleanup_hidden_files(is_windows_os())

        return self.pba_data
