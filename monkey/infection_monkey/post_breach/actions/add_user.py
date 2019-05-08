import datetime
from infection_monkey.post_breach.pba import PBA
from infection_monkey.config import WormConfiguration


__author__ = 'danielg'

LINUX_COMMANDS = ['useradd', '-M', '--expiredate',
                  datetime.datetime.today().strftime('%Y-%m-%d'), '--inactive', '0', '-c', 'MONKEY_USER',
                  WormConfiguration.user_to_add]

WINDOWS_COMMANDS = ['net', 'user', WormConfiguration.user_to_add,
                    WormConfiguration.remote_user_pass,
                    '/add', '/ACTIVE:NO']

PBA_NAME = "Backdoor user"


class BackdoorUser(object):
    def __init__(self):
        pass

    @staticmethod
    def get_pba():
        return PBA.default_get_pba(PBA_NAME, BackdoorUser, LINUX_COMMANDS, WINDOWS_COMMANDS)
