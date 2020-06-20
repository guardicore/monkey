from common.data.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.shell_startup_files.shell_startup_files_modification import\
    get_commands_to_modify_shell_startup_files
from infection_monkey.utils.environment import is_windows_os


class ModifyShellStartupFiles(PBA):
    """
    This PBA attempts to modify shell startup files,
    like ~/.profile, ~/.bashrc, ~/.bash_profile in linux,
    and profile.ps1 in windows.
    """

    def run(self):
        [pba.run() for pba in self.modify_shell_startup_PBA_list()]

    def modify_shell_startup_PBA_list(self):
        return ShellStartupPBAGenerator.get_modify_shell_startup_pbas()


class ShellStartupPBAGenerator():
    def get_modify_shell_startup_pbas():
        (cmds_for_linux, shell_startup_files_for_linux), windows_cmds = get_commands_to_modify_shell_startup_files()

        pbas = [ModifyShellStartupFile(linux_cmds='', windows_cmds=windows_cmds)]

        for shell_startup_file in shell_startup_files_for_linux:
            linux_cmds = ' '.join(cmds_for_linux).format(shell_startup_file)
            pbas.append(ModifyShellStartupFile(linux_cmds=linux_cmds, windows_cmds=''))

        return pbas


class ModifyShellStartupFile(PBA):
    def __init__(self, linux_cmds, windows_cmds):
        super(ModifyShellStartupFile, self).__init__(name=POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                                                     linux_cmd=linux_cmds,
                                                     windows_cmd=windows_cmds)
