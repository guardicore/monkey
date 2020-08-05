from common.data.post_breach_consts import POST_BREACH_BACKDOOR_USER
from infection_monkey.config import WormConfiguration
from infection_monkey.post_breach.pba import PBA
from infection_monkey.utils.users import get_commands_to_add_user


class BackdoorUser(PBA):
    def __init__(self):
        linux_cmds, windows_cmds = get_commands_to_add_user(
            WormConfiguration.user_to_add,
            WormConfiguration.remote_user_pass)
        super(BackdoorUser, self).__init__(
            POST_BREACH_BACKDOOR_USER,
            linux_cmd=' '.join(linux_cmds),
            windows_cmd=windows_cmds)
