TEMP_FILE = 'monkey-timestomping-file.txt'
TIMESTAMP_EPOCH = '197001010000.00'


def get_linux_timestomping_commands():
    return [
        f'echo "Successfully changed a file\'s modification timestamp" > {TEMP_FILE} && '
        f'touch -m -t {TIMESTAMP_EPOCH} {TEMP_FILE} && '
        f'cat {TEMP_FILE} ; '
        f'rm {TEMP_FILE} -f'
    ]


# Commands' source: https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1070.006/T1070.006.md
