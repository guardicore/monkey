TEMP_FILE = '$HOME/monkey-temp-file'

# Commands from https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1548.001/T1548.001.md


def get_linux_commands_to_setuid_setgid():
    return [
        f'touch {TEMP_FILE} && chown root {TEMP_FILE} && chmod u+s {TEMP_FILE} && chmod g+s {TEMP_FILE} &&',
        'echo "Successfully changed setuid/setgid bits" &&',
        f'rm {TEMP_FILE}'
    ]
