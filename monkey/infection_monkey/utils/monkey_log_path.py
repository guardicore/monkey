import os
import sys
import tempfile
import time
from functools import lru_cache


@lru_cache(maxsize=None)
def get_log_path(monkey_arg: str):
    return (
        os.path.expandvars(_generate_random_log_filepath(monkey_arg))
        if sys.platform == "win32"
        else _generate_random_log_filepath(monkey_arg)
    )


def _generate_random_log_filepath(monkey_arg: str) -> str:
    prefix = f"infection-monkey-{monkey_arg}-"
    suffix = f"-{time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())}.log"

    _, monkey_log_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)

    return monkey_log_path
