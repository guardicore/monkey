from infection_monkey.post_breach.trap_command.linux_trap_command import \
    get_linux_trap_commands


def get_trap_commands():
    linux_cmds = get_linux_trap_commands()
    return linux_cmds
