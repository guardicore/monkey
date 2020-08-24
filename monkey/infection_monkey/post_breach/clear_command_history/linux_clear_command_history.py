import subprocess

from infection_monkey.utils.environment import is_windows_os


def get_linux_commands_to_clear_command_history():
    if is_windows_os():
        return ''

    TEMP_HIST_FILE = '$HOME/monkey-temp-hist-file'

    return [
        '3<{0} 3<&- && ',  # check for existence of file
        'cat {0} '  # copy contents of history file to...
        f'> {TEMP_HIST_FILE} && ',  # ...temporary file
        'echo > {0} && ',  # clear contents of file
        'echo \"Successfully cleared {0}\" && ',  # if successfully cleared
        f'cat {TEMP_HIST_FILE} ',  # restore history file back with...
        '> {0} ;'  # ...original contents
        f'rm {TEMP_HIST_FILE} -f'  # remove temp history file
    ]


def get_linux_command_history_files():
    if is_windows_os():
        return []

    HOME_DIR = "/home/"

    # get list of paths of different shell history files (default values) with place for username
    STARTUP_FILES = [
        file_path.format(HOME_DIR) for file_path in
        [
            "{0}{{0}}/.bash_history",                       # bash
            "{0}{{0}}/.local/share/fish/fish_history",      # fish
            "{0}{{0}}/.zsh_history",                        # zsh
            "{0}{{0}}/.sh_history",                         # ksh
            "{0}{{0}}/.history"                             # csh, tcsh
        ]
    ]

    return STARTUP_FILES


def get_linux_usernames():
    if is_windows_os():
        return []

    # get list of usernames
    USERS = subprocess.check_output(  # noqa: DUO116
            "cut -d: -f1,3 /etc/passwd | egrep ':[0-9]{4}$' | cut -d: -f1",
            shell=True
        ).decode().split('\n')[:-1]

    return USERS
