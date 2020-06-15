SHELL_STARTUP_FILE = '$Profile'


def get_windows_commands_to_modify_shell_startup_files():
    return [
        'powershell.exe',  # run with powershell
        'Add-Content {0} '.format(SHELL_STARTUP_FILE),
        '\"# Successfully modified {0}\" ;'.format(SHELL_STARTUP_FILE),  # add line to $profile
        'cat {0} | Select -last 1 ;'.format(SHELL_STARTUP_FILE),  # print last line of $profile
        '$OldProfile = cat {0} | Select -skiplast 1 ;'.format(SHELL_STARTUP_FILE),
        'Set-Content {0} -Value $OldProfile ;'.format(SHELL_STARTUP_FILE)  # remove last line of $profile
]
