from infection_monkey.post_breach.shell_startup_files.linux.shell_startup_files_modification import (  # noqa: E501
    get_linux_commands_to_modify_shell_startup_files,
)
from infection_monkey.post_breach.shell_startup_files.windows.shell_startup_files_modification import (  # noqa: E501
    get_windows_commands_to_modify_shell_startup_files,
)


def get_commands_to_modify_shell_startup_files():
    linux_cmds = get_linux_commands_to_modify_shell_startup_files()
    windows_cmds = get_windows_commands_to_modify_shell_startup_files()
    return linux_cmds, windows_cmds
