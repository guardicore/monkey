import logging
import random
import time
from threading import Event, current_thread
from typing import Any, Dict, Sequence

import mock_dependency

from common.agent_events import ExploitationEvent, PropagationEvent
from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from infection_monkey.exploit import IAgentBinaryRepository
from infection_monkey.i_puppet import ExploiterResultData
from infection_monkey.model import TargetHost
from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository
from infection_monkey.utils.threading import interruptible_iter

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(
        self,
        agent_id: AgentID,
        agent_binary_repository: IAgentBinaryRepository,
        agent_event_publisher: IAgentEventPublisher,
        propagation_credentials_repository: IPropagationCredentialsRepository,
        plugin_name="",
    ):
        self._agent_id = agent_id
        self._agent_binary_repository = agent_binary_repository
        self._agent_event_publisher = agent_event_publisher
        self._propagation_credentials_repository = propagation_credentials_repository

    def run(
        self,
        host: TargetHost,
        servers: Sequence[str],
        current_depth: int,
        options: Dict[str, Any],
        interrupt: Event,
    ) -> ExploiterResultData:

        logger.info(f"Main thread name {current_thread().name}")
        logger.info(
            f"Mock dependency package version/operating system: {mock_dependency.__version__}"
        )

        Plugin._log_options(options)
        Plugin._sleep(options.get("sleep_duration", 0), interrupt)

        credentials = self._propagation_credentials_repository.get_credentials()
        credentials_str = "\n".join(map(str, credentials))
        logger.debug(f"Credentials: \n{credentials_str}")

        event_fields = {
            "source": self._agent_id,
            "target": host.ip,
            "exploiter_name": "Mock1Exploiter",
        }

        exploitation_success = self._exploit(options, event_fields)
        propagation_success = (
            False if not exploitation_success else self._propagate(options, event_fields)
        )

        logger.debug(f"Exploit success: {exploitation_success}")
        logger.debug(f"Prop success: {propagation_success}")
        logger.debug("OS: str(host.os)")
        exploiter_result_data = ExploiterResultData(
            exploitation_success=exploitation_success,
            propagation_success=propagation_success,
            os=str(host.operating_system),
        )
        logger.debug(f"Returning ExploiterResultData: {exploiter_result_data}")

        return exploiter_result_data

    @staticmethod
    def _log_options(options: Dict[str, Any]):
        logger.info("Plugin options:")

        list_of_strings = options.get("list_of_strings", None)
        logger.info(f"List of strings: {list_of_strings}")

        ssh_key = options.get("ssh_key", None)
        logger.info(f"SSH key: {ssh_key}")

        random_boolean = options.get("random_boolean", None)
        logger.info(f"Random boolean: {random_boolean}")

    @staticmethod
    def _sleep(duration: float, interrupt: Event):
        logger.info(f"Sleeping for {duration} seconds")
        for time_passed in interruptible_iter(range(int(duration)), interrupt):
            logger.info(f"Passed {time_passed} seconds")
            time.sleep(1)

    def _exploit(self, options: Dict[str, Any], event_fields: Dict[str, Any]) -> bool:
        exploitation_success = _get_random_result_from_success_rate("exploitation", options)
        self._agent_event_publisher.publish(
            ExploitationEvent(
                success=exploitation_success,
                tags=frozenset(["mock1-plugin-exploitation"]),
                **event_fields,
            )
        )

        return exploitation_success

    def _propagate(self, options: Dict[str, Any], event_fields: Dict[str, Any]) -> bool:
        propagation_success = _get_random_result_from_success_rate("propagation", options)
        self._agent_event_publisher.publish(
            PropagationEvent(
                success=propagation_success,
                tags=frozenset(["mock1-plugin-propagation"]),
                **event_fields,
            )
        )

        return propagation_success


def _get_random_result_from_success_rate(result_name: str, options: Dict[str, Any]) -> bool:
    success_rate = options.get(f"{result_name}_success_rate", 50)
    success_weights = [success_rate, 100 - success_rate]

    return random.choices([True, False], success_weights)[0]  # noqa: DUO102
