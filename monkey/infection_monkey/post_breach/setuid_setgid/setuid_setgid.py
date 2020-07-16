from infection_monkey.post_breach.setuid_setgid.linux_setuid_setgid import \
    get_linux_commands_to_setuid_setgid


def get_commands_to_change_setuid_setgid():
    linux_cmds = get_linux_commands_to_setuid_setgid()
    return linux_cmds
