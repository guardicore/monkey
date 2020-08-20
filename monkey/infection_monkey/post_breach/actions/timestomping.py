from common.data.post_breach_consts import POST_BREACH_TIMESTOMPPING
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.timestomping.timestomping import \
    get_timestomping_commands


class Timestomping(PBA):
    def __init__(self):
        linux_cmds, windows_cmds = get_timestomping_commands()
        super().__init__(POST_BREACH_TIMESTOMPPING,
                         linux_cmd=linux_cmds,
                         windows_cmd=windows_cmds)
