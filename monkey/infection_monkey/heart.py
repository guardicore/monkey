import logging
import time

from common.common_consts import HEARTBEAT_INTERVAL
from common.utils.code_utils import PeriodicCaller
from infection_monkey.island_api_client import IIslandAPIClient
from infection_monkey.utils.ids import get_agent_id

logger = logging.getLogger(__name__)


class Heart:
    def __init__(self, island_api_client: IIslandAPIClient):
        self._island_api_client = island_api_client
        self._periodic_caller = PeriodicCaller(
            self._send_heartbeats, HEARTBEAT_INTERVAL, "AgentHeart"
        )
        self._agent_id = get_agent_id()

    def start(self):
        logger.info("Starting the Agent's heart")
        self._periodic_caller.start()

    def _send_heartbeats(self):
        self._island_api_client.send_heartbeat(self._agent_id, time.time())

    def stop(self):
        logger.info("Stopping the Agent's heart")

        # Waiting HEARTBEAT_INTERVAL is more than enough time. In practice, stopping
        # self._periodic_caller should never take longer than it takes for
        # `self._island_api_client.send_heartbeat()` to timeout.
        self._periodic_caller.stop(timeout=HEARTBEAT_INTERVAL)
