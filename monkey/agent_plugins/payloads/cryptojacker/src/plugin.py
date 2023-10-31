import logging
from pprint import pformat
from typing import Any, Dict

from monkeytypes import AgentID, Event, SocketAddress

from common.event_queue import IAgentEventPublisher
from infection_monkey.i_puppet import PayloadResult

from .cryptojacker_builder import build_cryptojacker
from .cryptojacker_options import CryptojackerOptions

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(
        self,
        *,
        plugin_name="",
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
        island_server_address: SocketAddress,
        **kwargs,
    ):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher
        self._island_server_address = island_server_address

    def run(
        self,
        *,
        options: Dict[str, Any],
        interrupt: Event,
        **kwargs,
    ) -> PayloadResult:
        try:
            logger.debug(f"Parsing options: {pformat(options)}")
            cryptojacker_options = CryptojackerOptions(**options)
        except Exception as err:
            msg = f"Failed to parse Cryptojacker options: {err}"
            logger.exception(msg)
            return PayloadResult(success=False, error_message=msg)

        try:
            cryptojacker = build_cryptojacker(
                options=cryptojacker_options,
                agent_id=self._agent_id,
                agent_event_publisher=self._agent_event_publisher,
                island_server_address=self._island_server_address,
            )
        except Exception as err:
            msg = f"An unexpected error occurred while building the cryptojacker payload: {err}"
            logger.exception(msg)
            return PayloadResult(success=False, error_message=msg)

        try:
            cryptojacker.run(interrupt)
            return PayloadResult(success=True)
        except Exception as err:
            msg = f"An unexpected error occurred while running the cryptojacker payload: {err}"
            logger.exception(msg)
            return PayloadResult(success=False, error_message=msg)
