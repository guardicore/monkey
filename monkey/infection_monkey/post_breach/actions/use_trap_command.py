from common.data.post_breach_consts import POST_BREACH_TRAP_COMMAND
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.trap_command.trap_command import \
    get_trap_commands


class TrapCommand(PBA):
    def __init__(self):
        linux_cmds = get_trap_commands()
        super(TrapCommand, self).__init__(POST_BREACH_TRAP_COMMAND,
                                          linux_cmd=linux_cmds)
