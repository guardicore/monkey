import logging
import time
from threading import Event, current_thread
from typing import Any, Dict, Sequence

import mock_dependency
from monkeyevents import CredentialsStolenEvent
from monkeytypes import AgentID, Credentials, Password, Username

from common.event_queue import IAgentEventPublisher
from infection_monkey.utils.threading import interruptible_iter

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(
        self,
        *,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
        plugin_name="",
        **kwargs,
    ):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def run(
        self,
        *,
        options: Dict[str, Any],
        interrupt: Event,
        **kwargs,
    ):
        logger.info(f"Main thread name {current_thread().name}")
        logger.info(f"Mock dependency package version: {mock_dependency.__version__}")

        Plugin._log_options(options)
        Plugin._sleep(options.get("sleep_duration", 0), interrupt)

        return self._collect_credentials(options)

    @staticmethod
    def _log_options(options: Dict[str, Any]):
        logger.info("Plugin options:")

        random_boolean = options.get("random_boolean", None)
        logger.info(f"Random boolean: {random_boolean}")

    @staticmethod
    def _sleep(duration: float, interrupt: Event):
        logger.info(f"Sleeping for {duration} seconds")
        for time_passed in interruptible_iter(range(int(duration)), interrupt):
            logger.info(f"Passed {time_passed} seconds")
            time.sleep(1)

    def _collect_credentials(self, options: Dict[str, Any]) -> Sequence[Credentials]:
        collected_credentials = [
            Credentials(
                identity=Username(username="stolen_username"),
                secret=Password(password="stolen_password"),
            )
        ]
        self._agent_event_publisher.publish(
            CredentialsStolenEvent(
                stolen_credentials=collected_credentials,
                tags=frozenset(["mock1-plugin-collector"]),
                source=self._agent_id,
            )
        )
        return collected_credentials
