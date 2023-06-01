from common.agent_events import AbstractAgentEvent


class MessageEvent(AbstractAgentEvent):
    message: str
