import base64
import json
import logging
import random
import urllib.request
from typing import Optional

import urllib3

from common.event_queue import IAgentEventPublisher
from common.types import AgentID, SocketAddress
from common.utils.code_utils import PeriodicCaller
from infection_monkey.island_api_client.http_client import handle_island_errors

# Based on some very unofficial sources, it seems like 60 seconds is a good interval.
# https://bitcointalk.org/index.php?topic=1091724.0
REQUEST_INTERVAL = 60  # seconds


logger = logging.getLogger(__name__)


class BitcoinMiningNetworkTrafficSimulator:
    def __init__(
        self,
        island_server_address: SocketAddress,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
    ):
        self._island_server_address = island_server_address
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

        self._send_bitcoin_mining_request_periodically = PeriodicCaller(
            callback=self._send_bitcoin_mining_request,
            period=REQUEST_INTERVAL,
            name="Cryptojacking.BitcoinMiningNetworkTrafficSimulator",
        )

    def start(self):
        logger.info("Starting Bitcoin mining network traffic simulator")

        self._send_bitcoin_mining_request_periodically.start()

    @handle_island_errors
    def _send_bitcoin_mining_request(self):
        id_ = random.getrandbits(32)  # noqa: DUO102 (this isn't for cryptographic use)
        method = "getblocktemplate"
        params = [{"rules": ["segwit"]}]
        user = "bitcoin-user"
        password = "bitcoin-password"

        url = self._island_server_address
        data = json.dumps({"id": id_, "method": method, "params": params}).encode()
        auth = base64.encodebytes((user + ":" + password).encode()).decode().strip()

        logger.info(f"Sending Bitcoin mining request to {url}")

        request = urllib.request.Request(
            url=url, data=data, headers={"Authorization": "Basic {:s}".format(auth)}
        )
        urllib3.request.urlopen(request)

    def stop(self, timeout: Optional[float] = None):
        logger.info("Stopping Bitcoin mining network traffic simulator")

        self._send_bitcoin_mining_request_periodically.stop(timeout)
