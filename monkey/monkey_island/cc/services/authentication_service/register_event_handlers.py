from common import DIContainer
from common.agent_events import AbstractAgentEvent, AgentShutdownEvent
from common.event_queue import IAgentEventQueue
from common.types import AgentID
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic

from .authentication_facade import AuthenticationFacade


def register_event_handlers(container: DIContainer, authentication_facade: AuthenticationFacade):
    agent_event_queue = container.resolve(IAgentEventQueue)
    island_event_queue = container.resolve(IIslandEventQueue)

    agent_event_queue.subscribe_type(
        AgentShutdownEvent, unregister_agent_on_shutdown(authentication_facade)
    )
    island_event_queue.subscribe(
        IslandEventTopic.AGENT_TIMED_OUT, unregister_agent_on_timeout(authentication_facade)
    )


class unregister_agent_on_shutdown:
    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def __call__(self, event: AbstractAgentEvent):
        agent_id = event.source
        self._authentication_facade.remove_user(str(agent_id))


class unregister_agent_on_timeout:
    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def __call__(self, agent_id: AgentID):
        self._authentication_facade.remove_user(str(agent_id))
