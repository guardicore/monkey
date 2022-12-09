import logging
import random
from ipaddress import IPv4Address
from threading import Event
from typing import Any, Dict, Sequence

import bcrypt

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

    agent_id = get_agent_id()
    target = IPv4Address(host.ip_addr)
    name = "Test"
    exploitation_tags = "test-plugin-exploitation"
    propagation_tags = "test-plugin-propagation"
    os = host.os.get("type")

    success_choices = [True, False]

    logger.info(f"Package version: {bcrypt.__version__}")

    exploitation_success_rate = options.get("exploitation_success_rate", 50)
    exploitation_success_weights = [exploitation_success_rate, 100 - exploitation_success_rate]
    exploitation_success = random.choices(  # noqa: DUO102
        success_choices, exploitation_success_weights
    )
    exploitation_event = ExploitationEvent(
        source=agent_id,
        target=target,
        success=exploitation_success,
        exploiter_name=name,
        tags=exploitation_tags,
    )
    event_publisher.publish(exploitation_event)

    propagation_success = False

    if exploitation_success:
        propagation_success_rate = options.get("propagation_success_rate", 50)
        propagation_success_weights = [propagation_success_rate, 100 - propagation_success_rate]
        propagation_success = random.choices(  # noqa: DUO102
            success_choices, propagation_success_weights
        )
        propagation_event = PropagationEvent(
            source=agent_id,
            target=target,
            success=propagation_success,
            exploiter_name=name,
            tags=propagation_tags,
        )
        event_publisher.publish(propagation_event)

    return ExploiterResultData(
        exploitation_success=exploitation_success,
        propagation_success=propagation_success,
        os=os,
        info=None,
        error_message="",
    )
