import logging
import math
import os
import re
import subprocess
import sys

from common import OperatingSystem
from common.types import PingScanData
from infection_monkey.utils.environment import is_windows_os

TTL_REGEX = re.compile(r"TTL=([0-9]+)\b", re.IGNORECASE)
LINUX_TTL = 64  # Windows TTL is 128
PING_EXIT_TIMEOUT = 10
EMPTY_PING_SCAN = PingScanData(False, None)

logger = logging.getLogger(__name__)


def ping(host: str, timeout: float) -> PingScanData:
    try:
        return _ping(host, timeout)
    except Exception:
        logger.exception("Unhandled exception occurred while running ping")
        return EMPTY_PING_SCAN


def _ping(host: str, timeout: float) -> PingScanData:
    if is_windows_os():
        timeout = math.floor(timeout * 1000)

    ping_command_output = _run_ping_command(host, timeout)

    ping_scan_data = _process_ping_command_output(ping_command_output)
    logger.debug(f"{host} - {ping_scan_data}")

    return ping_scan_data


def _run_ping_command(host: str, timeout: float) -> str:
    ping_cmd = _build_ping_command(host, timeout)
    logger.debug(f"Running ping command: {' '.join(ping_cmd)}")

    # If stdout is not connected to a terminal (i.e. redirected to a pipe or file), the result
    # of os.device_encoding(1) will be None. Setting errors="backslashreplace" prevents a crash
    # in this case. See #1175 and #1403 for more information.
    encoding = os.device_encoding(1)
    sub_proc = subprocess.Popen(
        ping_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding=encoding,
        errors="backslashreplace",
    )

    logger.debug(f"Retrieving ping command output using {encoding} encoding")

    try:
        # The underlying ping command should timeout within the specified timeout. Setting the
        # timeout parameter on communicate() is a failsafe mechanism for ensuring this does not
        # block indefinitely.
        output = " ".join(sub_proc.communicate(timeout=(timeout + PING_EXIT_TIMEOUT)))
        logger.debug(output)
    except subprocess.TimeoutExpired as te:
        logger.error(te)
        return ""

    return output


def _process_ping_command_output(ping_command_output: str) -> PingScanData:
    ttl_match = TTL_REGEX.search(ping_command_output)
    if not ttl_match:
        return PingScanData(False, None)

    # It should be impossible for this next line to raise any errors, since the TTL_REGEX won't
    # match at all if the group isn't found or the contents of the group are not only digits.
    ttl = int(ttl_match.group(1))

    # could also be OSX/BSD, but lets handle that when it comes up.
    operating_system = OperatingSystem.LINUX if ttl <= LINUX_TTL else OperatingSystem.WINDOWS

    return PingScanData(True, operating_system)


def _build_ping_command(host: str, timeout: float):
    ping_count_flag = "-n" if "win32" == sys.platform else "-c"
    ping_timeout_flag = "-w" if "win32" == sys.platform else "-W"

    # on older version of ping the timeout must be an integer, thus we use ceil
    return ["ping", ping_count_flag, "1", ping_timeout_flag, str(math.ceil(timeout)), host]
