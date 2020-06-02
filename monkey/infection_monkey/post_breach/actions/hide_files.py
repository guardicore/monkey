import time
from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.hidden_files import\
    [get_commands_to_hide_files,
     get_commands_to_hide_folders] as CREATE_HIDDEN,\
    cleanup_hidden_files,\
    # get_winAPI_commands
from infection_monkey.utils.environment import is_windows_os


class HiddenFiles(PBA):
    """
    This PBA attempts to create hidden files and folders.
    """

    def __init__(self):
        pass

    def run(self):
        for method_to_create in CREATE_HIDDEN:
            linux_cmds, windows_cmds = method_to_create()
            super(HiddenFiles, self).__init__(name=POST_BREACH_HIDDEN_FILES,
                                              linux_cmd=' '.join(linux_cmds),
                                              window_cmd=windows_cmds)
        # if is_windows_os():
        #     get_winAPI_commands()
        #     PostBreachTelem(???)
        time.sleep(10)  # detection time for AV software
        cleanup_hidden_files(is_windows_os())
