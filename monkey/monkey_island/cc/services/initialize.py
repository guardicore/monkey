from pathlib import Path

from common import DIContainer
from common.aws import AWSInstance
from monkey_island.cc.repository import (
    AgentBinaryRepository,
    IAgentBinaryRepository,
    IFileRepository,
    LocalStorageFileRepository,
)
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services import AWSService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService

from . import AuthenticationService, JsonFileUserDatastore
from .reporting.report import ReportService

AGENT_BINARIES_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries"


def initialize_services(data_dir: Path) -> DIContainer:
    container = DIContainer()
    container.register_instance(AWSInstance, AWSInstance())

    container.register_instance(
        IFileRepository, LocalStorageFileRepository(data_dir / "custom_pbas")
    )
    container.register_instance(AWSService, container.resolve(AWSService))
    container.register_instance(IAgentBinaryRepository, _build_agent_binary_repository())

    # This is temporary until we get DI all worked out.
    PostBreachFilesService.initialize(container.resolve(IFileRepository))
    LocalMonkeyRunService.initialize(data_dir)
    AuthenticationService.initialize(data_dir, JsonFileUserDatastore(data_dir))
    ReportService.initialize(container.resolve(AWSService))

    return container


def _build_agent_binary_repository():
    file_repository = LocalStorageFileRepository(AGENT_BINARIES_PATH)
    return AgentBinaryRepository(file_repository)
