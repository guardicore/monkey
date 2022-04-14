import subprocess
from typing import Dict

from common.common_consts.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT
from infection_monkey.i_puppet.i_puppet import PostBreachData
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.shell_startup_files.shell_startup_files_modification import (
    get_commands_to_modify_shell_startup_files,
)
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class ModifyShellStartupFiles(PBA):
    """
    This PBA attempts to modify shell startup files,
    like ~/.profile, ~/.bashrc, ~/.bash_profile in linux,
    and profile.ps1 in windows.
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        super().__init__(telemetry_messenger, name=POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION)

    def run(self, options: Dict):
        results = [pba.run(options) for pba in self.modify_shell_startup_PBA_list()]
        if not results:
            results = [
                (
                    "Modify shell startup files PBA failed: Unable to find any regular users",
                    False,
                )
            ]
        # `command` is empty here since multiple commands were run through objects of the nested
        # class. The results of each of those were aggregated to send the telemetry just once.
        self.pba_data.append(PostBreachData(self.name, self.command, results))
        return self.pba_data

    @classmethod
    def modify_shell_startup_PBA_list(cls):
        return cls.ShellStartupPBAGenerator.get_modify_shell_startup_pbas()

    class ShellStartupPBAGenerator:
        @classmethod
        def get_modify_shell_startup_pbas(cls):
            (cmds_for_linux, shell_startup_files_for_linux, usernames_for_linux), (
                cmds_for_windows,
                shell_startup_files_per_user_for_windows,
            ) = get_commands_to_modify_shell_startup_files()

            pbas = []

            for startup_file_per_user in shell_startup_files_per_user_for_windows:
                windows_cmds = " ".join(cmds_for_windows).format(startup_file_per_user)
                pbas.append(cls.ModifyShellStartupFile(linux_cmds="", windows_cmds=windows_cmds))

            for username in usernames_for_linux:
                for shell_startup_file in shell_startup_files_for_linux:
                    linux_cmds = (
                        " ".join(cmds_for_linux).format(shell_startup_file).format(username)
                    )
                    pbas.append(cls.ModifyShellStartupFile(linux_cmds=linux_cmds, windows_cmds=""))

            return pbas

        class ModifyShellStartupFile(PBA):
            def __init__(self, linux_cmds, windows_cmds):
                super().__init__(
                    telemetry_messenger=None,
                    name=POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                    linux_cmd=linux_cmds,
                    windows_cmd=windows_cmds,
                )

            def run(self, options):
                if self.command:
                    try:
                        output = subprocess.check_output(  # noqa: DUO116
                            self.command,
                            stderr=subprocess.STDOUT,
                            shell=True,
                            timeout=LONG_REQUEST_TIMEOUT,
                        ).decode()

                        return output, True
                    except subprocess.CalledProcessError as err:
                        # Return error output of the command
                        return str(err), False
                    except subprocess.TimeoutExpired as err:
                        return str(err), False
