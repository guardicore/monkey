import threading
from typing import Callable, TypeAlias

from common.types import SocketAddress

CPUUtilizerCallable: TypeAlias = Callable[[threading.Event], None]
MemoryUtilizerCallable: TypeAlias = Callable[[threading.Event], None]
BitcoinMiningNetworkTrafficSimulatorCallable: TypeAlias = Callable[[SocketAddress], None]
