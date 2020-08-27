import subprocess

from common.data.post_breach_consts import POST_BREACH_CLEAR_CMD_HISTORY
from infection_monkey.post_breach.clear_command_history.clear_command_history import \
    get_commands_to_clear_command_history
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem


class ClearCommandHistory(PBA):
    def __init__(self):
        super().__init__(name=POST_BREACH_CLEAR_CMD_HISTORY)

    def run(self):
        results = [pba.run() for pba in self.clear_command_history_PBA_list()]
        if results:
            PostBreachTelem(self, results).send()

    def clear_command_history_PBA_list(self):
        return self.CommandHistoryPBAGenerator().get_clear_command_history_pbas()

    class CommandHistoryPBAGenerator():
        def get_clear_command_history_pbas(self):
            (cmds_for_linux, command_history_files_for_linux, usernames_for_linux) =\
             get_commands_to_clear_command_history()

            pbas = []

            for username in usernames_for_linux:
                for command_history_file in command_history_files_for_linux:
                    linux_cmds = ' '.join(cmds_for_linux).format(command_history_file).format(username)
                    pbas.append(self.ClearCommandHistoryFile(linux_cmds=linux_cmds))

            return pbas

        class ClearCommandHistoryFile(PBA):
            def __init__(self, linux_cmds):
                super().__init__(name=POST_BREACH_CLEAR_CMD_HISTORY,
                                 linux_cmd=linux_cmds)

            def run(self):
                if self.command:
                    try:
                        output = subprocess.check_output(self.command,  # noqa: DUO116
                                                         stderr=subprocess.STDOUT,
                                                         shell=True).decode()
                        return output, True
                    except subprocess.CalledProcessError as e:
                        # Return error output of the command
                        return e.output.decode(), False
