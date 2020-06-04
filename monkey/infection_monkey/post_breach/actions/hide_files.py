import time
from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.hidden_files import\
    get_commands_to_hide_files,\
    get_commands_to_hide_folders,\
    cleanup_hidden_files,\
    get_winAPI_to_hide_files
from infection_monkey.utils.environment import is_windows_os


CREATE_HIDDEN = [get_commands_to_hide_files,
                 get_commands_to_hide_folders]


class HiddenFiles(PBA):
    """
    This PBA attempts to create hidden files and folders.
    """

    def __init__(self):
        super(HiddenFiles, self).__init__(name=POST_BREACH_HIDDEN_FILES)

    def run(self):
        # create hidden files and folders
        for method_to_create in CREATE_HIDDEN:
            linux_cmds, windows_cmds = method_to_create()
            super(HiddenFiles, self).__init__(name=POST_BREACH_HIDDEN_FILES,
                                              linux_cmd=' '.join(linux_cmds),
                                              windows_cmd=windows_cmds)
            super(HiddenFiles, self).run()
        if is_windows_os():  # use winAPI
            result, status = get_winAPI_to_hide_files()
            PostBreachTelem(self, (result, status)).send()

        # detection time for AV software
        time.sleep(10)

        # cleanup hidden files and folders
        cleanup_hidden_files(is_windows_os())
