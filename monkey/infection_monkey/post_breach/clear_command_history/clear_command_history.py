from infection_monkey.post_breach.clear_command_history.linux_clear_command_history import (
    get_linux_command_history_files,
    get_linux_commands_to_clear_command_history, get_linux_usernames)


def get_commands_to_clear_command_history():
    (linux_cmds,
     linux_cmd_hist_files,
     linux_usernames) = (get_linux_commands_to_clear_command_history(),
                         get_linux_command_history_files(),
                         get_linux_usernames())
    return linux_cmds, linux_cmd_hist_files, linux_usernames
