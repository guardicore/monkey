import threading
from typing import Dict

from common.event_queue import IAgentEventQueue
from infection_monkey.payload.i_payload import IPayload

from . import ransomware_builder


class RansomwarePayload(IPayload):
    def __init__(self, agent_event_queue: IAgentEventQueue):
        self._agent_event_queue = agent_event_queue

    def run(self, options: Dict, interrupt: threading.Event):
        ransomware = ransomware_builder.build_ransomware(options, self._agent_event_queue)
        ransomware.run(interrupt)
