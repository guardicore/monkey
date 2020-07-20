from common.data.post_breach_consts import POST_BREACH_TRAP_COMMAND
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.trap_command.trap_command import \
    get_trap_commands
from infection_monkey.utils.environment import is_windows_os


class TrapCommand(PBA):
    def __init__(self):
        if not is_windows_os():
            linux_cmds = get_trap_commands()
            super(TrapCommand, self).__init__(POST_BREACH_TRAP_COMMAND,
                                              linux_cmd=linux_cmds)
