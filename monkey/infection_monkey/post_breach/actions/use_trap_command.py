from common.common_consts.post_breach_consts import POST_BREACH_TRAP_COMMAND
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.trap_command.trap_command import get_trap_commands
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class TrapCommand(PBA):
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        linux_cmds = get_trap_commands()
        super(TrapCommand, self).__init__(
            telemetry_messenger, POST_BREACH_TRAP_COMMAND, linux_cmd=" ".join(linux_cmds)
        )
