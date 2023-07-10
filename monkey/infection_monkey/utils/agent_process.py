import logging
import os
from typing import Optional

import psutil

from infection_monkey.island_api_client import IIslandAPIClient

logger = logging.getLogger(__name__)


def get_start_time() -> float:
    agent_process = psutil.Process(os.getpid())
    return agent_process.create_time()


def should_agent_stop(server: Optional[str], island_api_client: IIslandAPIClient) -> bool:
    if not server:
        logger.error("Agent should stop because it can't connect to the C&C server.")
        return True
    agent_signals = island_api_client.get_agent_signals()
    return agent_signals.terminate is not None
