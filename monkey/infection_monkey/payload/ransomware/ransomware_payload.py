from typing import Dict

from common.event_queue import IAgentEventQueue
from common.types import AgentID, Event
from infection_monkey.payload.i_payload import IPayload

from . import ransomware_builder


class RansomwarePayload(IPayload):
    def __init__(self, agent_event_queue: IAgentEventQueue, agent_id: AgentID):
        self._agent_event_queue = agent_event_queue
        self._agent_id = agent_id

    def run(self, options: Dict, interrupt: Event):
        ransomware = ransomware_builder.build_ransomware(
            options, self._agent_event_queue, self._agent_id
        )
        ransomware.run(interrupt)
