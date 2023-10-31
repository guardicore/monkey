from monkeytypes import AgentID
from ophidian import DIContainer

from common.agent_events import AbstractAgentEvent, AgentShutdownEvent
from common.event_queue import IAgentEventQueue
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic

from .authentication_facade import AuthenticationFacade


def register_event_handlers(container: DIContainer, authentication_facade: AuthenticationFacade):
    agent_event_queue = container.resolve(IAgentEventQueue)
    island_event_queue = container.resolve(IIslandEventQueue)
    agent_remover = AgentUserRemover(authentication_facade)

    agent_event_queue.subscribe_type(AgentShutdownEvent, agent_remover.remove_on_shutdown)
    island_event_queue.subscribe(IslandEventTopic.AGENT_TIMED_OUT, agent_remover.remove_on_timeout)


class AgentUserRemover:
    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def remove_on_shutdown(self, event: AbstractAgentEvent):
        agent_id = event.source
        self._authentication_facade.remove_user(str(agent_id))

    def remove_on_timeout(self, agent_id: AgentID):
        self._authentication_facade.remove_user(str(agent_id))
