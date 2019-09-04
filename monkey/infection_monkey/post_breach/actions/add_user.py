import datetime

from common.data.post_breach_consts import POST_BREACH_BACKDOOR_USER
from infection_monkey.post_breach.pba import PBA
from infection_monkey.config import WormConfiguration


class BackdoorUser(PBA):
    def __init__(self):
        linux_cmds, windows_cmds = BackdoorUser.get_commands_to_add_user(
            WormConfiguration.user_to_add, WormConfiguration.remote_user_pass)
        super(BackdoorUser, self).__init__(
            POST_BREACH_BACKDOOR_USER,
            linux_cmd=' '.join(linux_cmds),
            windows_cmd=windows_cmds)

    @staticmethod
    def get_commands_to_add_user(username, password):
        linux_cmds = BackdoorUser.get_linux_commands_to_add_user(username)
        windows_cmds = BackdoorUser.get_windows_commands_to_add_user(username, password)
        return linux_cmds, windows_cmds

    @staticmethod
    def get_linux_commands_to_add_user(username):
        linux_cmds = [
            'useradd',
            '-M',  # Do not create homedir
            '--expiredate',
            datetime.datetime.today().strftime('%Y-%m-%d'),
            '--inactive',
            '0',
            '-c',  # Comment
            'MONKEY_USER',  # Comment
            username]
        return linux_cmds

    @staticmethod
    def get_windows_commands_to_add_user(username, password, should_be_active=False):
        windows_cmds = [
            'net',
            'user',
            username,
            password,
            '/add']
        if not should_be_active:
            windows_cmds.append('/ACTIVE:NO')
        return windows_cmds
