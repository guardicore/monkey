from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic

from .file_agent_log_repository import FileAgentLogRepository
from .i_agent_log_repository import IAgentLogRepository


def setup_log_service(container: DIContainer):
    island_event_queue = container.resolve(IIslandEventQueue)
    repository = container.resolve(FileAgentLogRepository)
    container.register_instance(IAgentLogRepository, repository)

    _register_event_handlers(island_event_queue, repository)


def _register_event_handlers(
    island_event_queue: IIslandEventQueue, agent_log_repository: IAgentLogRepository
):
    island_event_queue.subscribe(IslandEventTopic.CLEAR_SIMULATION_DATA, agent_log_repository.reset)
