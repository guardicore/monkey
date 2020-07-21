from common.data.post_breach_consts import POST_BREACH_SETUID_SETGID
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.setuid_setgid.setuid_setgid import \
    get_commands_to_change_setuid_setgid
from infection_monkey.utils.environment import is_windows_os


class ChangeSetuidSetgid(PBA):
    def __init__(self):
        linux_cmds = get_commands_to_change_setuid_setgid()
        super(ChangeSetuidSetgid, self).__init__(POST_BREACH_SETUID_SETGID,
                                                 linux_cmd=' '.join(linux_cmds))
