from pathlib import Path

from flask_restful import Api

from ..i_agent_log_repository import IAgentLogRepository
from .agent_logs import AgentLogs
from .island_log import IslandLog


def register_resources(
    api: Api, agent_log_repository: IAgentLogRepository, island_log_file_path: Path
):
    api.add_resource(AgentLogs, *AgentLogs.urls, resource_class_args=(agent_log_repository,))
    api.add_resource(IslandLog, *IslandLog.urls, resource_class_args=(island_log_file_path,))
