import logging
import math
import os
import re
import subprocess
from ipaddress import IPv4Address
from time import time
from typing import Tuple

from agentpluginapi import PingScanData
from monkeyevents import PingScanEvent
from monkeytoolbox import get_os
from monkeytypes import AgentID, OperatingSystem

from common.event_queue import IAgentEventQueue

TTL_REGEX = re.compile(r"TTL=([0-9]+)\b", re.IGNORECASE)
LINUX_TTL = 64  # Windows TTL is 128
PING_EXIT_TIMEOUT = 10
EMPTY_PING_SCAN = PingScanData(response_received=False, os=None)

logger = logging.getLogger(__name__)


def ping(
    host: str, timeout: float, agent_event_queue: IAgentEventQueue, agent_id: AgentID
) -> PingScanData:
    try:
        return _ping(host, timeout, agent_event_queue, agent_id)
    except Exception:
        logger.exception("Unhandled exception occurred while running ping")
        return EMPTY_PING_SCAN


def _ping(
    host: str, timeout: float, agent_event_queue: IAgentEventQueue, agent_id: AgentID
) -> PingScanData:
    if get_os() == OperatingSystem.WINDOWS:
        timeout = math.floor(timeout * 1000)

    event_timestamp, ping_command_output = _run_ping_command(host, timeout)

    ping_scan_data = _process_ping_command_output(ping_command_output)
    logger.debug(f"{host} - {ping_scan_data}")

    ping_scan_event = _generate_ping_scan_event(host, ping_scan_data, event_timestamp, agent_id)
    agent_event_queue.publish(ping_scan_event)

    return ping_scan_data


def _run_ping_command(host: str, timeout: float) -> Tuple[float, str]:
    ping_cmd = _build_ping_command(host, timeout)
    logger.debug(f"Running ping command: {' '.join(ping_cmd)}")

    # If stdout is not connected to a terminal (i.e. redirected to a pipe or file), the result
    # of os.device_encoding(1) will be None. Setting errors="backslashreplace" prevents a crash
    # in this case. See #1175 and #1403 for more information.
    encoding = os.device_encoding(1)

    ping_event_timestamp = time()
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
        return ping_event_timestamp, ""

    return ping_event_timestamp, output


def _process_ping_command_output(ping_command_output: str) -> PingScanData:
    ttl_match = TTL_REGEX.search(ping_command_output)
    if not ttl_match:
        return PingScanData(response_received=False, os=None)

    # It should be impossible for this next line to raise any errors, since the TTL_REGEX won't
    # match at all if the group isn't found or the contents of the group are not only digits.
    ttl = int(ttl_match.group(1))

    # could also be OSX/BSD, but lets handle that when it comes up.
    operating_system = OperatingSystem.LINUX if ttl <= LINUX_TTL else OperatingSystem.WINDOWS

    return PingScanData(response_received=True, os=operating_system)


def _build_ping_command(host: str, timeout: float):
    ping_count_flag = "-n" if (get_os() == OperatingSystem.WINDOWS) else "-c"
    ping_timeout_flag = "-w" if (get_os() == OperatingSystem.WINDOWS) else "-W"

    # on older version of ping the timeout must be an integer, thus we use ceil
    return ["ping", ping_count_flag, "1", ping_timeout_flag, str(math.ceil(timeout)), host]


def _generate_ping_scan_event(
    host: str, ping_scan_data: PingScanData, event_timestamp: float, agent_id: AgentID
) -> PingScanEvent:
    # TODO: Tag with the appropriate MITRE ATT&CK tags
    return PingScanEvent(
        source=agent_id,
        target=IPv4Address(host),
        timestamp=event_timestamp,
        response_received=ping_scan_data.response_received,
        os=ping_scan_data.os,
    )
