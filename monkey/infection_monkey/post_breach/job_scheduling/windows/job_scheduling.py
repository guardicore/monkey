SCHEDULED_TASK_NAME = 'monkey-spawn-cmd'
SCHEDULED_TASK_COMMAND = 'C:\windows\system32\cmd.exe'


def get_windows_commands_to_schedule_jobs():
    return [
        'schtasks',
        '/Create',
        '/SC',
        'monthly',
        '/TN',
        SCHEDULED_TASK_NAME,
        '/TR',
        SCHEDULED_TASK_COMMAND
    ]


def get_windows_commands_to_remove_scheduled_jobs():
    return [
        'schtasks',
        '/Delete',
        '/TN',
        SCHEDULED_TASK_NAME,
        '/F',
        '>',
        'nul',
        '2>&1'
    ]
