STARTUP_FILES = [
    "~/.profile",  # bash, dash, ksh, sh
    "~/.bashrc", "~/.bash_profile",  # bash
    "~/.config/fish/config.fish",  # fish
    "~/.zshrc", "~/.zshenv", "~/.zprofile",  # zsh
    "~/.kshrc",  # ksh
    "~/.tcshrc",  # tcsh
    "~/.cshrc",  # csh
    ]


def get_linux_commands_to_modify_shell_startup_files():
    return [
        'echo \"# Succesfully modified {0}\"',
        '3<{0} 3<&- |',  # check for existence of file
        'tee -a',  # append to file
        '{0}',
        '&&',
        'sed -i \'$d\' {0}',  # remove last line of file
    ],\
     STARTUP_FILES
