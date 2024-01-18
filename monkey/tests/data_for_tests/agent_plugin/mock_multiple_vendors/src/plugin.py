import logging
from threading import Event, current_thread
from typing import Any, Dict, Sequence

import mock_dependency
from agentpluginapi import ExploiterResult, IAgentBinaryRepository, TargetHost
from monkeyevents import ExploitationEvent
from monkeytypes import AgentID

from common.event_queue import IAgentEventPublisher
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
        logger.info(
            f"Mock dependency package version/operating system: {mock_dependency.__version__}"
        )

        self._agent_event_publisher.publish(
            ExploitationEvent(
                source=self._agent_id,
                target=host.ip,
                exploiter_name="MockWithMultipleVendorsExploiter",
                success=False,
                tags=frozenset(["mock-with-multiple-vendors-plugin-exploitation"]),
            )
        )

        exploiter_result = ExploiterResult(
            exploitation_success=False,
            propagation_success=False,
            os=str(host.operating_system),
        )
        logger.debug(f"Returning ExploiterResult: {exploiter_result}")

        return exploiter_result
