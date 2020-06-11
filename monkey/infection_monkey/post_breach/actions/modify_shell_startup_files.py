from common.data.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from infection_monkey.post_breach.pba import PBA
from infection_monkey.utils.shell_startup_files_modification import\
    get_commands_to_modify_shell_startup_files
from infection_monkey.utils.environment import is_windows_os


class ModifyShellStartupFiles(PBA):
    """
    This PBA attempts to modify shell startup files,
    like ~/.profile, ~/.bashrc, ~/.bash_profile in linux,
    and profile.ps1 in windows.
    """

    def __init__(self):
        super(ModifyShellStartupFiles, self).__init__(name=POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION)

    def run(self):
        (cmds_for_linux, shell_startup_files_for_linux), windows_cmds = get_commands_to_modify_shell_startup_files()

        if is_windows_os():
            super(ModifyShellStartupFiles, self).__init__(name=POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                                                          linux_cmd=' '.join(linux_cmds),
                                                          windows_cmd=windows_cmds)
            super(ModifyShellStartupFiles, self).run()
        else:
            for shell_startup_file in shell_startup_files_for_linux:
                linux_cmds = ' '.join(cmds_for_linux).format(shell_startup_file)
                super(ModifyShellStartupFiles, self).__init__(name=POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                                                              linux_cmd=linux_cmds,
                                                              windows_cmd=windows_cmds)
                super(ModifyShellStartupFiles, self).run()
