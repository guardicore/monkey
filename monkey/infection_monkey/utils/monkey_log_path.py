import tempfile
import time
from functools import lru_cache, partial
from pathlib import Path


# Cache the result of the call so that subsequent calls always return the same result
@lru_cache(maxsize=None)
def _get_log_path(monkey_arg: str) -> Path:
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    prefix = f"infection-monkey-{monkey_arg}-{timestamp}-"
    suffix = ".log"

    _, monkey_log_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)

    return Path(monkey_log_path)


get_agent_log_path = partial(_get_log_path, "agent")
get_dropper_log_path = partial(_get_log_path, "dropper")
