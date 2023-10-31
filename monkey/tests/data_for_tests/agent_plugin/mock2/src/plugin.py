import logging
from threading import Event, current_thread
from typing import Any, Dict, Sequence

import mock_dependency
from monkeytypes import AgentID

from common.agent_events import ExploitationEvent, PropagationEvent
from common.event_queue import IAgentEventPublisher
from infection_monkey.exploit import IAgentBinaryRepository
from infection_monkey.i_puppet import ExploiterResult, TargetHost
from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(
        self,
        *,
        agent_id: AgentID,
        agent_binary_repository: IAgentBinaryRepository,
        agent_event_publisher: IAgentEventPublisher,
        propagation_credentials_repository: IPropagationCredentialsRepository,
        plugin_name="",
        **kwargs,
    ):
        self._agent_id = agent_id
        self._agent_binary_repository = agent_binary_repository
        self._agent_event_publisher = agent_event_publisher
        self._propagation_credentials_repository = propagation_credentials_repository

    def run(
        self,
        *,
        host: TargetHost,
        servers: Sequence[str],
        current_depth: int,
        options: Dict[str, Any],
        interrupt: Event,
        **kwargs,
    ) -> ExploiterResult:
        logger.info(f"Main thread name {current_thread().name}")
        logger.info(f"Mock dependency package version: {mock_dependency.__version__}")

        Plugin._log_options(options)

        credentials = self._propagation_credentials_repository.get_credentials()
        credentials_str = "\n".join(map(str, credentials))
        logger.debug(f"Credentials: \n{credentials_str}")

        event_fields = {
            "source": self._agent_id,
            "target": host.ip,
            "exploiter_name": "Mock2Exploiter",
        }

        exploitation_success = self._exploit(options, event_fields)
        propagation_success = (
            False if not exploitation_success else self._propagate(options, event_fields)
        )

        logger.debug(f"Exploit success: {exploitation_success}")
        logger.debug(f"Prop success: {propagation_success}")
        logger.debug(f"OS: {str(host.operating_system)}")
        exploiter_result = ExploiterResult(
            exploitation_success=exploitation_success,
            propagation_success=propagation_success,
            os=str(host.operating_system),
        )
        logger.debug(f"Returning ExploiterResult: {exploiter_result}")

        return exploiter_result

    @staticmethod
    def _log_options(options: Dict[str, Any]):
        logger.info("Plugin options:")

        list_of_strings = options.get("list_of_strings", None)
        logger.info(f"List of strings: {list_of_strings}")

        exploitation_success = options.get("exploitation_success", None)
        logger.info(f"Exploitation success will be: {exploitation_success}")

        propagation_success = options.get("propagation_success", False)
        logger.info(f"Propagation success will be: {propagation_success}")

    def _exploit(self, options: Dict[str, Any], event_fields: Dict[str, Any]) -> bool:
        exploitation_success = options.get("exploitation_success", False)
        self._agent_event_publisher.publish(
            ExploitationEvent(
                success=exploitation_success,
                tags=frozenset(["mock2-plugin-exploitation"]),
                **event_fields,
            )
        )

        return exploitation_success

    def _propagate(self, options: Dict[str, Any], event_fields: Dict[str, Any]) -> bool:
        propagation_success = options.get("propagation_success", False)
        self._agent_event_publisher.publish(
            PropagationEvent(
                success=propagation_success,
                tags=frozenset(["mock2-plugin-propagation"]),
                **event_fields,
            )
        )

        return propagation_success
