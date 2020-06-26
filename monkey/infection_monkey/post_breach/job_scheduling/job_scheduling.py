from infection_monkey.post_breach.job_scheduling.linux.job_scheduling import\
    get_linux_commands_to_schedule_jobs
from infection_monkey.post_breach.job_scheduling.windows.job_scheduling import\
    get_windows_commands_to_schedule_jobs


def get_commands_to_schedule_jobs():
    linux_cmds = get_linux_commands_to_schedule_jobs()
    windows_cmds = get_windows_commands_to_schedule_jobs()
    return linux_cmds, windows_cmds
