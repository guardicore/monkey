import logging
import time

from infection_monkey.island_api_client import IIslandAPIClient
from infection_monkey.utils.ids import get_agent_id
from infection_monkey.utils.threading import create_daemon_thread

HEARTBEAT_INTERVAL = 30

logger = logging.getLogger(__name__)


class Heart:
    def __init__(self, island_api_client: IIslandAPIClient):
        self._island_api_client = island_api_client
        self._heartbeat_thread = create_daemon_thread(
            target=self._send_heartbeats, name="HeartbeatThread"
        )
        self._agent_id = get_agent_id()

    def start(self):
        logger.debug("Starting the Agent's heart")
        self._heartbeat_thread.start()

    def _send_heartbeats(self):
        while True:
            self._island_api_client.send_heartbeat(self._agent_id, time.time())
            time.sleep(HEARTBEAT_INTERVAL)

    def stop(self):
        logger.debug("Stopping the Agent's heart")
        self._heartbeat_thread.join(timeout=0)
