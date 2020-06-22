import subprocess
from infection_monkey.utils.environment import is_windows_os


def get_windows_commands_to_modify_shell_startup_files():
    if not is_windows_os():
        return '', []

    # get powershell startup file path
    SHELL_STARTUP_FILE = subprocess.check_output('powershell $Profile').decode().split("\r\n")[0]
    SHELL_STARTUP_FILE_PATH_COMPONENTS = SHELL_STARTUP_FILE.split("\\")

    # get list of usernames
    USERS = subprocess.check_output('dir C:\\Users /b', shell=True).decode().split("\r\n")[:-1]

    STARTUP_FILES_PER_USER = ['\\'.join(SHELL_STARTUP_FILE_PATH_COMPONENTS[:2] +
                                        [user] +
                                        SHELL_STARTUP_FILE_PATH_COMPONENTS[3:])
                              for user in USERS]

    return [
        'Add-Content {0}',
        '\"# Successfully modified {0}\" ;',  # add line to $profile
        'cat {0} | Select -last 1 ;',  # print last line of $profile
        '$OldProfile = cat {0} | Select -skiplast 1 ;',
        'Set-Content {0} -Value $OldProfile ;'  # remove last line of $profile
    ], STARTUP_FILES_PER_USER
