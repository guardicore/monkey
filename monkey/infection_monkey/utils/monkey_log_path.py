import os
import sys
import tempfile
import time
from functools import lru_cache, partial
from pathlib import Path


# Cache the result of the call so that subsequent calls always return the same result
@lru_cache(maxsize=None)
def _get_log_path(monkey_arg: str) -> Path:
    return Path(
        os.path.expandvars(_generate_random_log_filepath(monkey_arg))
        if sys.platform == "win32"
        else _generate_random_log_filepath(monkey_arg)
    )


def _generate_random_log_filepath(monkey_arg: str) -> str:
    prefix = f"infection-monkey-{monkey_arg}-"
    suffix = f"-{time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())}.log"

    _, monkey_log_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)

    return monkey_log_path


get_agent_log_path = partial(_get_log_path, "monkey")
get_dropper_log_path = partial(_get_log_path, "dropper")
