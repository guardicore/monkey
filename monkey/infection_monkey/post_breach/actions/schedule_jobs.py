from typing import Dict

from common.common_consts.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from infection_monkey.post_breach.job_scheduling.job_scheduling import (
    get_commands_to_schedule_jobs,
    remove_scheduled_jobs,
)
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class ScheduleJobs(PBA):
    """
    This PBA attempts to schedule jobs on the system.
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        linux_cmds, windows_cmds = get_commands_to_schedule_jobs()

        super(ScheduleJobs, self).__init__(
            telemetry_messenger,
            name=POST_BREACH_JOB_SCHEDULING,
            linux_cmd=" ".join(linux_cmds),
            windows_cmd=windows_cmds,
        )

    def run(self, options: Dict):
        super(ScheduleJobs, self).run(options)
        remove_scheduled_jobs()
        return self.pba_data
