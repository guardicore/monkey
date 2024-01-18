import logging
from pprint import pformat
from typing import Any, Dict

from agentpluginapi import LocalMachineInfo, PayloadResult
from monkeytypes import AgentID, Event

from common.event_queue import IAgentEventPublisher

from .ransomware_builder import build_ransomware
from .ransomware_options import RansomwareOptions

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(
        self,
        *,
        plugin_name="",
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
        local_machine_info: LocalMachineInfo,
        **kwargs,
    ):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher
        self._local_machine_info = local_machine_info

    def run(
        self,
        *,
        options: Dict[str, Any],
        interrupt: Event,
        **kwargs,
    ) -> PayloadResult:
        try:
            logger.debug(f"Parsing options: {pformat(options)}")
            ransomware_options = RansomwareOptions(**options)
        except Exception as err:
            msg = f"Failed to parse Ransomware options: {err}"
            logger.exception(msg)
            return PayloadResult(success=False, error_message=msg)

        try:
            ransomware = build_ransomware(
                self._agent_id,
                self._agent_event_publisher,
                ransomware_options,
                self._local_machine_info.operating_system,
            )
        except Exception as err:
            msg = f"An unexpected error occurred while building the ransomware payload: {err}"
            logger.exception(msg)
            return PayloadResult(success=False, error_message=msg)

        try:
            ransomware.run(interrupt)
            return PayloadResult(success=True)
        except Exception as err:
            msg = f"An unexpected error occurred while running the ransomware payload: {err}"
            logger.exception(msg)
            return PayloadResult(success=False, error_message=msg)
