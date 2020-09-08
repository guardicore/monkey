import subprocess

from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.linux.hidden_files import (
    get_linux_commands_to_delete, get_linux_commands_to_hide_files,
    get_linux_commands_to_hide_folders)
from infection_monkey.utils.windows.hidden_files import (
    get_windows_commands_to_delete, get_windows_commands_to_hide_files,
    get_windows_commands_to_hide_folders)


def get_commands_to_hide_files():
    linux_cmds = get_linux_commands_to_hide_files()
    windows_cmds = get_windows_commands_to_hide_files()
    return linux_cmds, windows_cmds


def get_commands_to_hide_folders():
    linux_cmds = get_linux_commands_to_hide_folders()
    windows_cmds = get_windows_commands_to_hide_folders()
    return linux_cmds, windows_cmds


def cleanup_hidden_files(is_windows=is_windows_os()):
    subprocess.run(get_windows_commands_to_delete() if is_windows  # noqa: DUO116
                   else ' '.join(get_linux_commands_to_delete()),
                   shell=True)
