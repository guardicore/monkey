# isort: off
# Serpentarium resets the import state to a default state each
# time a plugin is run.
# The following import has objects that are used for communication between the Agent and plugins,
# and need to be imported before serpentarium so that they are added to the default
# import state. This prevents pickling errors. Without this, when a plugin is run,
# we'll get errors like
# "_pickle.PicklingError: Can't pickle <class 'xyz': it's not the same object as xyz".
import infection_monkey.agent_plugin_api_imports  # noqa: F401
import infection_monkey.monkey_events_imports  # noqa: F401
from common.command_builder import (  # noqa: F401
    LinuxDownloadMethod,
    LinuxDownloadOptions,
    LinuxRunOptions,
    AgentMode,
    WindowsDownloadMethod,
    WindowsDownloadOptions,
    WindowsRunOptions,
    WindowsShell,
    ILinuxAgentCommandBuilder,
    IWindowsAgentCommandBuilder,
    IAgentCommandBuilderFactory,
)

# UPDATE: It's the second import now; read comment above
# serpentarium must be the first import, as it needs to save the state of the
# import system prior to any imports
import serpentarium  # noqa: F401
from serpentarium.logging import configure_host_process_logger

# isort: on
import argparse
import logging
import logging.handlers
import os
import re
import sys
import tempfile
import time
import traceback
from multiprocessing import Queue, freeze_support, get_context
from pathlib import Path
from typing import Sequence, Tuple, Union

from psutil import Process

# dummy import for pyinstaller
# noinspection PyUnresolvedReferences
from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE
from common.version import get_version
from infection_monkey.dropper import MonkeyDrops
from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.monkey import InfectionMonkey


class OTPFormatter(logging.Formatter):
    """
    Formatter that replaces OTPs in log messages with asterisks
    """

    OTP_REGEX = re.compile(f"{AGENT_OTP_ENVIRONMENT_VARIABLE}=\\S+[\\s;]+")
    OTP_REPLACEMENT = f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={'*' * 6}"

    def format(self, record):
        original_log_message = logging.Formatter.format(self, record)
        formatted_log_message = re.sub(
            OTPFormatter.OTP_REGEX, OTPFormatter.OTP_REPLACEMENT, original_log_message
        )

        return formatted_log_message


def main():
    freeze_support()  # required for multiprocessing + pyinstaller on windows

    mode, mode_specific_args = _parse_args()

    # TODO: Use an Enum for this
    if mode not in [MONKEY_ARG, DROPPER_ARG]:
        raise ValueError(f'The mode argument must be either "{MONKEY_ARG}" or "{DROPPER_ARG}"')

    multiprocessing_context = get_context(method="spawn")
    ipc_logger_queue = multiprocessing_context.Queue()

    log_path = _create_secure_log_file(mode)

    queue_listener = _configure_queue_listener(ipc_logger_queue, log_path)
    queue_listener.start()

    logger = _configure_logger()
    logger.info(f"writing log file to {log_path}")

    try:
        _run_agent(mode, mode_specific_args, ipc_logger_queue, logger, log_path)
    except Exception as err:
        logger.exception(f"An unexpected error occurred while running the agent: {err}")
    finally:
        logger.debug("Stopping the queue listener")
        queue_listener.stop()


def _parse_args() -> Tuple[str, Sequence[str]]:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "mode",
        choices=[MONKEY_ARG, DROPPER_ARG],
        help=f"'{MONKEY_ARG}' mode will run the agent in the current session/terminal."
        f"'{DROPPER_ARG}' will detach the agent from the current session "
        f"and will start it on a separate process.",
    )
    mode_args, mode_specific_args = arg_parser.parse_known_args()
    mode = str(mode_args.mode)

    return mode, mode_specific_args


def _create_secure_log_file(monkey_arg: str) -> Path:
    """
    Create and cache secure log file

    :param monkey_arg: Argument for the agent. Possible `agent` or `dropper`
    :return: Path of the secure log file
    """
    mode = "agent" if monkey_arg == MONKEY_ARG else "dropper"
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    prefix = f"infection-monkey-{mode}-{timestamp}-"
    suffix = ".log"

    handle, monkey_log_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(handle)

    return Path(monkey_log_path)


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
    formatter = OTPFormatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    queue_listener = configure_host_process_logger(ipc_logger_queue, [stream_handler, file_handler])
    return queue_listener


def _configure_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    def log_uncaught_exceptions(ex_cls, ex, tb):
        logger.critical("".join(traceback.format_tb(tb)))
        logger.critical("{0}: {1}".format(ex_cls, ex))

    sys.excepthook = log_uncaught_exceptions

    return logger


def _run_agent(
    mode: str,
    mode_specific_args: Sequence[str],
    ipc_logger_queue: Queue,
    logger: logging.Logger,
    log_path: Path,
):
    logger.info(
        ">>>>>>>>>> Initializing the Infection Monkey Agent: PID %s <<<<<<<<<<", os.getpid()
    )

    logger.info(f"version: {get_version()}")

    monkey: Union[InfectionMonkey, MonkeyDrops]
    if mode == MONKEY_ARG:
        monkey = InfectionMonkey(
            mode_specific_args, ipc_logger_queue=ipc_logger_queue, log_path=log_path
        )
    elif mode == DROPPER_ARG:
        monkey = MonkeyDrops(mode_specific_args)

    try:
        logger.info(f"Starting {monkey.__class__.__name__}")
        monkey.start()
    except Exception as err:
        logger.exception("Exception thrown from monkey's start function. More info: {}".format(err))

    try:
        monkey.cleanup()
    except Exception as err:
        logger.exception(
            "Exception thrown from monkey's cleanup function: More info: {}".format(err)
        )
    finally:
        if mode == MONKEY_ARG:
            _kill_hung_child_processes(logger)


def _kill_hung_child_processes(logger: logging.Logger):
    for p in Process().children(recursive=True):
        logger.debug(
            "Found child process: "
            f"pid={p.pid}, name={p.name()}, status={p.status()}, cmdline={p.cmdline()}"
        )

        if _process_is_resource_tracker(p):
            # This process will clean itself up, but no other processes should be running at
            # this time.
            logger.debug(f"Ignoring resource_tracker process: {p.pid}")
            continue

        if _process_is_windows_self_removal(p):
            logger.debug(f"Ignoring self removal process: {p.pid}")
            continue

        logger.warning(f"Killing hung child process: {p.pid}")
        p.kill()


def _process_is_resource_tracker(process: Process) -> bool:
    for arg in process.cmdline():
        if "multiprocessing.resource_tracker" in arg:
            return True

    return False


def _process_is_windows_self_removal(process: Process) -> bool:
    if process.name() in ["cmd.exe", "timeout.exe"]:
        return True

    return False


if "__main__" == __name__:
    main()
