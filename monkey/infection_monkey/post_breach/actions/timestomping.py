from common.common_consts.post_breach_consts import POST_BREACH_TIMESTOMPING
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.timestomping.timestomping import get_timestomping_commands
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class Timestomping(PBA):
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        linux_cmds, windows_cmds = get_timestomping_commands()
        super().__init__(
            telemetry_messenger,
            POST_BREACH_TIMESTOMPING,
            linux_cmd=linux_cmds,
            windows_cmd=windows_cmds,
        )
