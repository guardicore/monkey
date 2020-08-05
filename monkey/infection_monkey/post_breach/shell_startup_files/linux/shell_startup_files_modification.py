import subprocess

from infection_monkey.utils.environment import is_windows_os


def get_linux_commands_to_modify_shell_startup_files():
    if is_windows_os():
        return '', [], []

    HOME_DIR = "/home/"

    # get list of usernames
    USERS = subprocess.check_output(  # noqa: DUO116
            "cut -d: -f1,3 /etc/passwd | egrep ':[0-9]{4}$' | cut -d: -f1",
            shell=True
        ).decode().split('\n')[:-1]

    # get list of paths of different shell startup files with place for username
    STARTUP_FILES = [
        file_path.format(HOME_DIR) for file_path in
        [
            "{0}{{0}}/.profile",                    # bash, dash, ksh, sh
            "{0}{{0}}/.bashrc",                     # bash
            "{0}{{0}}/.bash_profile",
            "{0}{{0}}/.config/fish/config.fish",    # fish
            "{0}{{0}}/.zshrc",                      # zsh
            "{0}{{0}}/.zshenv",
            "{0}{{0}}/.zprofile",
            "{0}{{0}}/.kshrc",                      # ksh
            "{0}{{0}}/.tcshrc",                     # tcsh
            "{0}{{0}}/.cshrc",                      # csh
        ]
    ]

    return [
        '3<{0} 3<&- &&',  # check for existence of file
        'echo \"# Succesfully modified {0}\" |',
        'tee -a {0} &&',  # append to file
        'sed -i \'$d\' {0}',  # remove last line of file (undo changes)
    ], STARTUP_FILES, USERS
