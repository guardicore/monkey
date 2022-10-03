import logging
from typing import Optional

from common.agent_events import PropagationEvent
from infection_monkey.network.relay import TCPRelay

logger = logging.getLogger(__name__)


class notify_relay_on_propagation:
    def __init__(self, tcp_relay: Optional[TCPRelay]):
        self._tcp_relay = tcp_relay

    def __call__(self, event: PropagationEvent):
        if self._tcp_relay is None:
            return

        if event.success:
            self._tcp_relay.add_potential_user(event.target)
