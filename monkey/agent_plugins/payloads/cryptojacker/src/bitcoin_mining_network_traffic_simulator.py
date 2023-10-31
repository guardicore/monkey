import base64
import json
import logging
import random
import time
from http import HTTPMethod
from typing import Optional

import requests
from monkeytypes import AgentID, SocketAddress
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout

from common.agent_events import HTTPRequestEvent
from common.event_queue import IAgentEventPublisher
from common.utils.code_utils import PeriodicCaller

from .consts import CRYPTOJACKER_PAYLOAD_TAG

# Based on some very unofficial sources, it seems like 60 seconds is a good interval.
# https://bitcointalk.org/index.php?topic=1091724.0
REQUEST_INTERVAL = 60  # seconds
BITCOIN_MINING_REQUEST_TIMEOUT = 5  # seconds

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
            callback=self.send_bitcoin_mining_request,
            period=REQUEST_INTERVAL,
            name="Cryptojacking.BitcoinMiningNetworkTrafficSimulator",
        )

        self._headers = BitcoinMiningNetworkTrafficSimulator._build_headers()

    @staticmethod
    def _build_headers():
        user = "bitcoin-user"
        password = "bitcoin-password"
        auth = base64.encodebytes((user + ":" + password).encode()).decode().strip()

        return {
            "Accept-Encoding": "identity",
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def start(self):
        logger.info("Starting Bitcoin mining network traffic simulator")

        self._send_bitcoin_mining_request_periodically.start()

    def send_bitcoin_mining_request(self):
        url = f"http://{self._island_server_address}/"
        failure_warning_msg = f"Failed to establish a connection with {url}"
        body = json.dumps(
            BitcoinMiningNetworkTrafficSimulator._build_getblocktemplate_request_body()
        ).encode()

        logger.info(f"Sending Bitcoin mining request to {url}")

        timestamp = time.time()
        try:
            requests.post(
                url,
                data=body,
                headers=self._headers,
                timeout=BITCOIN_MINING_REQUEST_TIMEOUT,
            )
        except ConnectTimeout as err:
            logger.warning(f"{failure_warning_msg}: {err}")
        except (ReadTimeout, ConnectionResetError):
            self._publish_http_request_event(timestamp, url)
        except ConnectionError as err:
            self._handle_connection_error(err, timestamp, url, failure_warning_msg)

    @staticmethod
    def _build_getblocktemplate_request_body():
        id_ = random.getrandbits(32)  # noqa: DUO102 (this isn't for cryptographic use)
        method = "getblocktemplate"
        params = [{"rules": ["segwit"]}]

        return {"id": id_, "method": method, "params": params}

    def _publish_http_request_event(self, timestamp: float, url: str):
        http_request_event = HTTPRequestEvent(
            source=self._agent_id,
            timestamp=timestamp,
            tags=frozenset({CRYPTOJACKER_PAYLOAD_TAG}),
            method=HTTPMethod.POST,
            url=url,  # type: ignore [arg-type]
        )
        self._agent_event_publisher.publish(http_request_event)

    def _handle_connection_error(
        self, err: ConnectionError, timestamp: float, url: str, failure_warning_msg: str
    ):
        try:
            expected_connection_reset_error = (
                err.__context__.__context__
            )  # ignore: type [union-attr]
            if isinstance(expected_connection_reset_error, ConnectionResetError):
                self._publish_http_request_event(timestamp, url)
            else:
                logger.warning(f"{failure_warning_msg}: {err}")
        except AttributeError:
            logger.warning(f"{failure_warning_msg}: {err}")

    def stop(self, timeout: Optional[float] = None):
        logger.info("Stopping Bitcoin mining network traffic simulator")

        self._send_bitcoin_mining_request_periodically.stop(timeout)
