import logging
import subprocess
from typing import Iterable, Tuple

from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT
from infection_monkey.post_breach.job_scheduling.linux_job_scheduling import (
    get_linux_commands_to_schedule_jobs,
)
from infection_monkey.post_breach.job_scheduling.windows_job_scheduling import (
    get_windows_commands_to_remove_scheduled_jobs,
    get_windows_commands_to_schedule_jobs,
)
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)


def get_commands_to_schedule_jobs() -> Tuple[Iterable[str], str]:
    linux_cmds = get_linux_commands_to_schedule_jobs()
    windows_cmds = get_windows_commands_to_schedule_jobs()
    return linux_cmds, windows_cmds


def remove_scheduled_jobs():
    if is_windows_os():
        try:
            subprocess.run(  # noqa: DUO116
                get_windows_commands_to_remove_scheduled_jobs(),
                timeout=LONG_REQUEST_TIMEOUT,
                shell=True,
            )
        except subprocess.CalledProcessError as err:
            logger.error(f"An error occurred while removing scheduled jobs on Windows: {err}")
        except subprocess.TimeoutExpired as err:
            logger.error(f"A timeout occurred while removing scheduled jobs on Windows: {err}")
