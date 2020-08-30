from infection_monkey.utils.linux.users import get_linux_commands_to_add_user
from infection_monkey.utils.windows.users import \
    get_windows_commands_to_add_user


def get_commands_to_add_user(username, password):
    linux_cmds = get_linux_commands_to_add_user(username)
    windows_cmds = get_windows_commands_to_add_user(username, password)
    return linux_cmds, windows_cmds
