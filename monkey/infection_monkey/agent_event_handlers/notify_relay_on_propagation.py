import logging
from typing import Optional

from monkeyevents import PropagationEvent

from infection_monkey.network.relay import TCPRelay

logger = logging.getLogger(__name__)


class notify_relay_on_propagation:
    """
    Notifies a TCPRelay of potential relay users if propagation is successful
    """

    def __init__(self, tcp_relay: Optional[TCPRelay]):
        """
        :param tcp_relay: A TCPRelay to notify on successful propagation
        """
        self._tcp_relay = tcp_relay

    def __call__(self, event: PropagationEvent):
        """
        Notify a TCPRelay of potential relay users if propagation is successful

        :param event: A `PropagationEvent`
        """
        if self._tcp_relay is None:
            return

        if event.success:
            self._tcp_relay.add_potential_user(event.target)
