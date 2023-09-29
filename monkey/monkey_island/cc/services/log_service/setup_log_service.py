from pathlib import Path

from flask_restful import Api
from ophidian import DIContainer

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.server_utils.island_logger import get_log_file_path

from .file_agent_log_repository import FileAgentLogRepository
from .flask_resources import register_resources
from .i_agent_log_repository import IAgentLogRepository


def setup_log_service(api: Api, container: DIContainer, data_dir: Path):
    island_event_queue = container.resolve(IIslandEventQueue)
    repository = container.resolve(FileAgentLogRepository)
    container.register_instance(IAgentLogRepository, repository)
    island_log_file_path = get_log_file_path(data_dir)

    _register_event_handlers(island_event_queue, repository)
    register_resources(api, repository, island_log_file_path)


def _register_event_handlers(
    island_event_queue: IIslandEventQueue, agent_log_repository: IAgentLogRepository
):
    island_event_queue.subscribe(IslandEventTopic.CLEAR_SIMULATION_DATA, agent_log_repository.reset)
