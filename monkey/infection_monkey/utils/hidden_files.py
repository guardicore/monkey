import subprocess
from infection_monkey.utils.linux.hidden_files import\
    get_linux_commands_to_hide_files,\
    get_linux_commands_to_hide_folders,\
    get_linux_commands_to_delete
from infection_monkey.utils.windows.hidden_files import\
    get_windows_commands_to_hide_files,\
    get_windows_commands_to_hide_folders,\
    get_winAPI_to_hide_files,\
    get_windows_commands_to_delete,\
    get_winAPI_to_delete_files
from infection_monkey.utils.environment import is_windows_os


def get_commands_to_hide_files():
    linux_cmds = get_linux_commands_to_hide_files()
    windows_cmds = get_windows_commands_to_hide_files()
    return linux_cmds, windows_cmds


def get_commands_to_hide_folders():
    linux_cmds = get_linux_commands_to_hide_folders()
    windows_cmds = get_windows_commands_to_hide_folders()
    return linux_cmds, windows_cmds


def get_winAPI_to_hide_files():
    get_winAPI_to_hide_files()


def cleanup_hidden_files(is_windows=is_windows_os()):
    if is_windows:
        get_winAPI_to_delete_files()
    subprocess.run(get_windows_commands_to_delete() if is_windows
                   else get_linux_commands_to_delete())
