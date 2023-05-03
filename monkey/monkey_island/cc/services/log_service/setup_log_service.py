from flask_restful import Api

from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic

from .file_agent_log_repository import FileAgentLogRepository
from .flask_resources.register_resources import register_resources
from .i_agent_log_repository import IAgentLogRepository


def setup_log_service(api: Api, container: DIContainer):
    island_event_queue = container.resolve(IIslandEventQueue)
    repository = container.resolve(FileAgentLogRepository)
    container.register_instance(IAgentLogRepository, repository)

    _register_event_handlers(island_event_queue, repository)
    register_resources(api, container, repository)


def _register_event_handlers(
    island_event_queue: IIslandEventQueue, agent_log_repository: IAgentLogRepository
):
    island_event_queue.subscribe(IslandEventTopic.CLEAR_SIMULATION_DATA, agent_log_repository.reset)
