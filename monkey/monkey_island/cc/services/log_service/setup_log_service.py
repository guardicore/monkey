from common import DIContainer

from .file_agent_log_repository import FileAgentLogRepository
from .i_agent_log_repository import IAgentLogRepository


def setup_log_service(container: DIContainer):
    container.register_instance(IAgentLogRepository, container.resolve(FileAgentLogRepository))
