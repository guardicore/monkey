from infection_monkey.post_breach.clear_command_history.linux_clear_command_history import \
    get_linux_commands_to_clear_command_history


def get_commands_to_clear_command_history():
    linux_cmds = get_linux_commands_to_clear_command_history()
    return linux_cmds
