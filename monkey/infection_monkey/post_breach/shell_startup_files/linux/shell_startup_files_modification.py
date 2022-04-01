import logging
import subprocess

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)


def get_linux_commands_to_modify_shell_startup_files():
    if is_windows_os():
        return "", [], []

    home_dir = "/home/"
    command = "cut -d: -f1,3 /etc/passwd | egrep ':[0-9]{4}$' | cut -d: -f1"

    # get list of usernames
    try:
        users = (
            subprocess.check_output(  # noqa: DUO116
                command,
                shell=True,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
            .decode()
            .split("\n")[:-1]
        )
    except subprocess.TimeoutExpired:
        logger.error(f"Command {command} timed out")
        return "", [], []

    # get list of paths of different shell startup files with place for username
    startup_files = [
        file_path.format(home_dir)
        for file_path in [
            "{0}{{0}}/.profile",  # bash, dash, ksh, sh
            "{0}{{0}}/.bashrc",  # bash
            "{0}{{0}}/.bash_profile",
            "{0}{{0}}/.config/fish/config.fish",  # fish
            "{0}{{0}}/.zshrc",  # zsh
            "{0}{{0}}/.zshenv",
            "{0}{{0}}/.zprofile",
            "{0}{{0}}/.kshrc",  # ksh
            "{0}{{0}}/.tcshrc",  # tcsh
            "{0}{{0}}/.cshrc",  # csh
        ]
    ]

    return (
        [
            "3<{0} 3<&- &&",  # check for existence of file
            'echo "# Succesfully modified {0}" |',
            "tee -a {0} &&",  # append to file
            "sed -i '$d' {0}",  # remove last line of file (undo changes)
        ],
        startup_files,
        users,
    )
