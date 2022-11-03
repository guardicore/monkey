import logging

from urllib3 import disable_warnings

from common.types import SocketAddress

disable_warnings()  # noqa DUO131

logger = logging.getLogger(__name__)


class ControlClient:
    def __init__(self, server_address: SocketAddress):
        self.server_address = server_address
