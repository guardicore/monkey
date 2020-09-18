SCHEDULED_TASK_NAME = 'monkey-spawn-cmd'
SCHEDULED_TASK_COMMAND = r'C:\windows\system32\cmd.exe'

# Commands from: https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1053.005/T1053.005.md


def get_windows_commands_to_schedule_jobs():
    return f'schtasks /Create /SC monthly /TN {SCHEDULED_TASK_NAME} /TR {SCHEDULED_TASK_COMMAND}'


def get_windows_commands_to_remove_scheduled_jobs():
    return f'schtasks /Delete /TN {SCHEDULED_TASK_NAME} /F > nul 2>&1'
