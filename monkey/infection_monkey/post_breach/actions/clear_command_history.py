import subprocess
from typing import Dict, Iterable, Tuple

from common.common_consts.post_breach_consts import POST_BREACH_CLEAR_CMD_HISTORY
from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT
from infection_monkey.i_puppet.i_puppet import PostBreachData
from infection_monkey.post_breach.clear_command_history.clear_command_history import (
    get_commands_to_clear_command_history,
)
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class ClearCommandHistory(PBA):
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        super().__init__(telemetry_messenger, name=POST_BREACH_CLEAR_CMD_HISTORY)

    def run(self, options: Dict) -> Iterable[PostBreachData]:
        results = [pba.run() for pba in self.clear_command_history_pba_list()]
        if results:
            # `self.command` is empty here
            self.pba_data.append(PostBreachData(self.name, self.command, results))

        return self.pba_data

    def clear_command_history_pba_list(self) -> Iterable[PBA]:
        return self.CommandHistoryPBAGenerator().get_clear_command_history_pbas()

    class CommandHistoryPBAGenerator:
        def get_clear_command_history_pbas(self) -> Iterable[PBA]:
            (
                cmds_for_linux,
                command_history_files_for_linux,
                usernames_for_linux,
            ) = get_commands_to_clear_command_history()

            pbas = []

            for username in usernames_for_linux:
                for command_history_file in command_history_files_for_linux:
                    linux_cmds = (
                        " ".join(cmds_for_linux).format(command_history_file).format(username)
                    )
                    pbas.append(self.ClearCommandHistoryFile(linux_cmds=linux_cmds))

            return pbas

        class ClearCommandHistoryFile(PBA):
            def __init__(self, linux_cmds):
                super().__init__(
                    telemetry_messenger=None,
                    name=POST_BREACH_CLEAR_CMD_HISTORY,
                    linux_cmd=linux_cmds,
                )

            def run(self) -> Tuple[str, bool]:
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
                        return err.output.decode(), False
                    except subprocess.TimeoutExpired as err:
                        return str(err), False
