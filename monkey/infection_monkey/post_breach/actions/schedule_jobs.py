from common.data.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from infection_monkey.post_breach.job_scheduling.job_scheduling import (
    get_commands_to_schedule_jobs, remove_scheduled_jobs)
from infection_monkey.post_breach.pba import PBA


class ScheduleJobs(PBA):
    """
    This PBA attempts to schedule jobs on the system.
    """

    def __init__(self):
        linux_cmds, windows_cmds = get_commands_to_schedule_jobs()

        super(ScheduleJobs, self).__init__(name=POST_BREACH_JOB_SCHEDULING,
                                           linux_cmd=' '.join(linux_cmds),
                                           windows_cmd=windows_cmds)

        remove_scheduled_jobs()
