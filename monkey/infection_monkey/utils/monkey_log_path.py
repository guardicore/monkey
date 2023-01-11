import os
import tempfile
import time
from functools import lru_cache, partial
from pathlib import Path


# Cache the result of the call so that subsequent calls always return the same result
@lru_cache(maxsize=None)
def _create_secure_log_file(monkey_arg: str) -> Path:
    """
    Create and cache secure log file

    :param monkey_arg: Argument for the agent. Possible `agent` or `dropper`
    :return: Path of the secure log file
    """
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    prefix = f"infection-monkey-{monkey_arg}-{timestamp}-"
    suffix = ".log"

    handle, monkey_log_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(handle)

    return Path(monkey_log_path)


create_secure_agent_log_file = partial(_create_secure_log_file, "agent")
create_secure_dropper_log_file = partial(_create_secure_log_file, "dropper")
