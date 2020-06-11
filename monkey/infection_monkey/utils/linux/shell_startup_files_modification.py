BASH_STARTUP_FILES = ["~/.bashrc", "~/.profile", "~/.bash_profile"]


def get_linux_commands_to_modify_shell_startup_files():
    return [
        'if [ -f {0} ] ;',  # does the file exist?
        'then',
        'echo \"# Succesfully modified {0}\" |',
        'tee -a',
        '{0}',  # add comment to file
        '&&',
        'sed -i \'$d\' {0} ;',  # remove last line of file
        'else',
        'echo \"{0} does not exist\" ; fi'  # mention if file does not exist
    ],\
    BASH_STARTUP_FILES
