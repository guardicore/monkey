import shutil
import tempfile
from pathlib import Path

MONKEY_DIR_PREFIX = "monkey_dir_"
_monkey_dir = None


# TODO: Check if we even need this. Individual plugins can just use tempfile.mkdtemp() or
#       tempfile.mkftemp() if they need to.
def create_monkey_dir() -> Path:
    """
    Creates directory for monkey and related files
    """
    global _monkey_dir

    _monkey_dir = Path(tempfile.mkdtemp(prefix=MONKEY_DIR_PREFIX, dir=tempfile.gettempdir()))
    return _monkey_dir


def remove_monkey_dir() -> bool:
    """
    Removes monkey's root directory
    :return True if removed without errors and False otherwise
    """
    try:
        shutil.rmtree(get_monkey_dir_path())
        return True
    except Exception:
        return False


def get_monkey_dir_path() -> Path:
    if _monkey_dir is None:
        create_monkey_dir()

    return _monkey_dir  # type: ignore
