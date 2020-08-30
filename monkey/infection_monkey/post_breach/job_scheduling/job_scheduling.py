import subprocess

from infection_monkey.post_breach.job_scheduling.linux_job_scheduling import \
    get_linux_commands_to_schedule_jobs
from infection_monkey.post_breach.job_scheduling.windows_job_scheduling import (
    get_windows_commands_to_remove_scheduled_jobs,
    get_windows_commands_to_schedule_jobs)
from infection_monkey.utils.environment import is_windows_os


def get_commands_to_schedule_jobs():
    linux_cmds = get_linux_commands_to_schedule_jobs()
    windows_cmds = get_windows_commands_to_schedule_jobs()
    return linux_cmds, windows_cmds


def remove_scheduled_jobs():
    if is_windows_os():
        subprocess.run(get_windows_commands_to_remove_scheduled_jobs(), shell=True)  # noqa: DUO116
