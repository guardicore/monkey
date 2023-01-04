# serpentarium must be the first import, as it needs to save the state of the
# import system prior to any imports
# isort: off
import serpentarium  # noqa: F401
from serpentarium.logging import configure_host_process_logger

# isort: on
import argparse
import logging
import logging.handlers
import os
import sys
import traceback
from multiprocessing import Queue, freeze_support, get_context
from pathlib import Path

# dummy import for pyinstaller
# noinspection PyUnresolvedReferences
from common.version import get_version
from infection_monkey.dropper import MonkeyDrops
from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.monkey import InfectionMonkey
from infection_monkey.utils.monkey_log_path import get_agent_log_path, get_dropper_log_path


def main():
    freeze_support()  # required for multiprocessing + pyinstaller on windows

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "mode",
        choices=[MONKEY_ARG, DROPPER_ARG],
        help=f"'{MONKEY_ARG}' mode will run the agent in the current session/terminal."
        f"'{DROPPER_ARG}' will detach the agent from the current session "
        f"and will start it on a separate process.",
    )
    mode_args, mode_specific_args = arg_parser.parse_known_args()
    mode = mode_args.mode

    try:
        if MONKEY_ARG == mode:
            log_path = get_agent_log_path()
            monkey_cls = InfectionMonkey
        elif DROPPER_ARG == mode:
            log_path = get_dropper_log_path()
            monkey_cls = MonkeyDrops
        else:
            return True
    except ValueError:
        return True

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    multiprocessing_context = get_context(method="spawn")
    ipc_logger_queue = multiprocessing_context.Queue()

    queue_listener = _configure_queue_listener(ipc_logger_queue, log_path)
    queue_listener.start()

    def log_uncaught_exceptions(ex_cls, ex, tb):
        logger.critical("".join(traceback.format_tb(tb)))
        logger.critical("{0}: {1}".format(ex_cls, ex))

    sys.excepthook = log_uncaught_exceptions

    logger.info(
        ">>>>>>>>>> Initializing monkey (%s): PID %s <<<<<<<<<<", monkey_cls.__name__, os.getpid()
    )

    logger.info(f"version: {get_version()}")
    logger.info(f"writing log file to {log_path}")

    monkey = monkey_cls(mode_specific_args)

    try:
        monkey.start()
    except Exception as err:
        logger.exception("Exception thrown from monkey's start function. More info: {}".format(err))

    try:
        monkey.cleanup()
    except Exception as err:
        logger.exception(
            "Exception thrown from monkey's cleanup function: More info: {}".format(err)
        )

    queue_listener.stop()


def _configure_queue_listener(
    ipc_logger_queue: Queue, log_file_path: Path
) -> logging.handlers.QueueListener:
    """
    Gets unstarted configured QueueListener object

    We configure the root logger to use QueueListener with Stream and File handler.

    :param ipc_logger_queue: A Queue shared by the host and child process that stores log messages
    :param log_path: A Path used to configure the FileHandler
    """
    log_format = (
        "%(asctime)s [%(process)d:%(threadName)s:%(levelname)s] %(module)s.%("
        "funcName)s.%(lineno)d: %(message)s"
    )
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    queue_listener = configure_host_process_logger(ipc_logger_queue, [stream_handler, file_handler])
    return queue_listener


if "__main__" == __name__:
    if not main():
        sys.exit(1)
