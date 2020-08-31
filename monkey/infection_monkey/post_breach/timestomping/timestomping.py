from infection_monkey.post_breach.timestomping.linux.timestomping import \
    get_linux_timestomping_commands
from infection_monkey.post_breach.timestomping.windows.timestomping import \
    get_windows_timestomping_commands


def get_timestomping_commands():
    linux_cmds = get_linux_timestomping_commands()
    windows_cmds = get_windows_timestomping_commands()
    return linux_cmds, windows_cmds
