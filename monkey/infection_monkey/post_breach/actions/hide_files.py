from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.hidden_files import (cleanup_hidden_files,
                                                 get_commands_to_hide_files,
                                                 get_commands_to_hide_folders)
from infection_monkey.utils.windows.hidden_files import \
    get_winAPI_to_hide_files

HIDDEN_FSO_CREATION_COMMANDS = [get_commands_to_hide_files,
                                get_commands_to_hide_folders]


class HiddenFiles(PBA):
    """
    This PBA attempts to create hidden files and folders.
    """

    def __init__(self):
        super(HiddenFiles, self).__init__(name=POST_BREACH_HIDDEN_FILES)

    def run(self):
        # create hidden files and folders
        for function_to_get_commands in HIDDEN_FSO_CREATION_COMMANDS:
            linux_cmds, windows_cmds = function_to_get_commands()
            super(HiddenFiles, self).__init__(name=POST_BREACH_HIDDEN_FILES,
                                              linux_cmd=' '.join(linux_cmds),
                                              windows_cmd=windows_cmds)
            super(HiddenFiles, self).run()
        if is_windows_os():  # use winAPI
            result, status = get_winAPI_to_hide_files()
            PostBreachTelem(self, (result, status)).send()

        # cleanup hidden files and folders
        cleanup_hidden_files(is_windows_os())
