import subprocess

from infection_monkey.utils.environment import is_windows_os


def get_windows_commands_to_modify_shell_startup_files():
    if not is_windows_os():
        return '', []

    # get powershell startup file path
    SHELL_STARTUP_FILE = subprocess.check_output('powershell $Profile').decode().split("\r\n")[0]
    SHELL_STARTUP_FILE_PATH_COMPONENTS = SHELL_STARTUP_FILE.split("\\")

    # get list of usernames
    USERS = subprocess.check_output('dir C:\\Users /b', shell=True).decode().split("\r\n")[:-1]  # noqa: DUO116
    USERS.remove("Public")

    STARTUP_FILES_PER_USER = ['\\'.join(SHELL_STARTUP_FILE_PATH_COMPONENTS[:2] +
                                        [user] +
                                        SHELL_STARTUP_FILE_PATH_COMPONENTS[3:])
                              for user in USERS]

    return [
        'powershell.exe',
        'infection_monkey/post_breach/shell_startup_files/windows/modify_powershell_startup_file.ps1',
        '-startup_file_path {0}'
    ], STARTUP_FILES_PER_USER
