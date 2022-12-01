import logging
import time
from threading import Event

from common.common_consts import HEARTBEAT_INTERVAL
from infection_monkey.island_api_client import IIslandAPIClient
from infection_monkey.utils.ids import get_agent_id
from infection_monkey.utils.threading import create_daemon_thread

logger = logging.getLogger(__name__)


class Heart:
    def __init__(self, island_api_client: IIslandAPIClient):
        self._island_api_client = island_api_client
        self._heartbeat_thread = create_daemon_thread(
            target=self._send_heartbeats, name="HeartbeatThread"
        )
        self._agent_id = get_agent_id()
        self._stop = Event()

    def start(self):
        logger.debug("Starting the Agent's heart")
        self._heartbeat_thread.start()

    def _send_heartbeats(self):
        logger.info("Agent's heart started")

        while not self._stop.is_set():
            self._island_api_client.send_heartbeat(self._agent_id, time.time())
            self._stop.wait(HEARTBEAT_INTERVAL)

        logger.info("Agent's heart stopped")

    def stop(self):
        logger.debug("Stopping the Agent's heart")
        self._stop.set()

        # Waiting HEARTBEAT_INTERVAL is more than enough time. In practice, this join() should never
        # take longer than it takes for `send_heartbeat()`'s to timeout.
        self._heartbeat_thread.join(timeout=HEARTBEAT_INTERVAL)
        if self._heartbeat_thread.is_alive():
            logger.warning("Timed out waiting for the agent's heart to stop")
