import logging
import random
from ipaddress import IPv4Address
from threading import Event
from typing import Any, Dict, Sequence

import mock_dependency

from common.agent_events import ExploitationEvent, PropagationEvent
from common.event_queue import IAgentEventPublisher
from infection_monkey.exploit import IAgentBinaryRepository
from infection_monkey.i_puppet import ExploiterResultData
from infection_monkey.model import VictimHost
from infection_monkey.utils.ids import get_agent_id

logger = logging.getLogger(__name__)


def run(
    host: VictimHost,
    servers: Sequence[str],
    current_depth: int,
    options: Dict[str, Any],
    interrupt: Event,
    agent_binary_repository: IAgentBinaryRepository,
    event_publisher: IAgentEventPublisher,
) -> ExploiterResultData:

    logger.info(f"Mock dependency package version: {mock_dependency.__version__}")

    event_fields = {
        "source": get_agent_id(),
        "target": IPv4Address(host.ip_addr),
        "exploiter_name": "MockExploiter",
    }

    exploitation_success = _get_random_result_from_success_rate("exploitation", options)
    event_publisher.publish(
        ExploitationEvent(
            success=exploitation_success,
            tags=frozenset(["mock-plugin-exploitation"]),
            **event_fields,
        )
    )

    propagation_success = _get_random_result_from_success_rate("propagation", options)
    event_publisher.publish(
        PropagationEvent(
            success=propagation_success,
            tags=frozenset(["mock-plugin-propagation"]),
            **event_fields,
        )
    )

    return ExploiterResultData(
        exploitation_success=exploitation_success,
        propagation_success=propagation_success,
        os=host.os.get("type"),
    )


def _get_random_result_from_success_rate(result_name: str, options: Dict[str, Any]):
    success_rate = options.get(f"{result_name}_success_rate", 50)
    success_weights = [success_rate, 100 - success_rate]

    return random.choices([True, False], success_weights)  # noqa: DUO102
