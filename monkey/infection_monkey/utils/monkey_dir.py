import os
import shutil
import tempfile

from infection_monkey.config import WormConfiguration


def create_monkey_dir():
    """
    Creates directory for monkey and related files
    """
    if not os.path.exists(get_monkey_dir_path()):
        os.mkdir(get_monkey_dir_path())


def remove_monkey_dir():
    """
    Removes monkey's root directory
    :return True if removed without errors and False otherwise
    """
    try:
        shutil.rmtree(get_monkey_dir_path())
        return True
    except Exception:
        return False


def get_monkey_dir_path():
    return os.path.join(tempfile.gettempdir(), WormConfiguration.monkey_dir_name)
