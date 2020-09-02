TEMP_FILE = 'monkey-timestomping-file.txt'


def get_windows_timestomping_commands():
    return 'powershell.exe infection_monkey/post_breach/timestomping/windows/timestomping.ps1'


# Commands' source: https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1070.006/T1070.006.md
