from common.common_consts.post_breach_consts import POST_BREACH_BACKDOOR_USER
from infection_monkey.config import WormConfiguration
from infection_monkey.post_breach.pba import PBA
from infection_monkey.utils.random_password_generator import get_random_password
from infection_monkey.utils.users import get_commands_to_add_user


class BackdoorUser(PBA):
    def __init__(self):
        random_password = get_random_password()

        linux_cmds, windows_cmds = get_commands_to_add_user(
            WormConfiguration.user_to_add, random_password
        )

        super(BackdoorUser, self).__init__(
            POST_BREACH_BACKDOOR_USER, linux_cmd=" ".join(linux_cmds), windows_cmd=windows_cmds
        )
