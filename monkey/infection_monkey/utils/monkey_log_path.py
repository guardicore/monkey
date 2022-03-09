import os
import string
import sys
import time
from random import SystemRandom

from infection_monkey.config import WormConfiguration


def get_monkey_log_path():
    return (
        os.path.expandvars(
            _generate_random_log_filepath(WormConfiguration.monkey_log_directory_windows, "agent")
        )
        if sys.platform == "win32"
        else _generate_random_log_filepath(WormConfiguration.monkey_log_directory_linux, "agent")
    )


def get_dropper_log_path():
    return (
        os.path.expandvars(
            _generate_random_log_filepath(
                WormConfiguration.dropper_log_directory_windows, "dropper"
            )
        )
        if sys.platform == "win32"
        else _generate_random_log_filepath(WormConfiguration.dropper_log_directory_linux, "dropper")
    )


def _generate_random_log_filepath(log_directory: str, monkey_arg: str) -> str:
    safe_random = SystemRandom()
    random_string = "".join(
        [safe_random.choice(string.ascii_lowercase + string.digits) for _ in range(8)]
    )
    prefix = f"infection-monkey-{monkey_arg}-"
    suffix = f"-{time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())}.log"
    log_file_path = os.path.join(log_directory, prefix + random_string + suffix)

    return log_file_path
