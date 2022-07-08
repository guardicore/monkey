import logging
from pathlib import Path

from common import DIContainer
from common.aws import AWSInstance
from common.configuration import (
    DEFAULT_AGENT_CONFIGURATION,
    DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
    AgentConfiguration,
)
from common.utils.file_utils import get_binary_io_sha256_hash
from monkey_island.cc.repository import (
    AgentBinaryRepository,
    FileAgentConfigurationRepository,
    FileRepositoryCachingDecorator,
    FileRepositoryLockingDecorator,
    FileRepositoryLoggingDecorator,
    FileSimulationRepository,
    IAgentBinaryRepository,
    IAgentConfigurationRepository,
    ICredentialsRepository,
    IFileRepository,
    ISimulationRepository,
    LocalStorageFileRepository,
    MongoCredentialsRepository,
    RetrievalError,
)
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services import AWSService, IslandModeService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService

from . import AuthenticationService, JsonFileUserDatastore
from .reporting.report import ReportService

logger = logging.getLogger(__name__)

AGENT_BINARIES_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries"


def initialize_services(data_dir: Path) -> DIContainer:
    container = DIContainer()
    _register_conventions(container, data_dir)
    container.register_instance(AWSInstance, AWSInstance())
    _register_repositories(container, data_dir)
    _register_services(container)

    # This is temporary until we get DI all worked out.
    PostBreachFilesService.initialize(container.resolve(IFileRepository))
    AuthenticationService.initialize(data_dir, JsonFileUserDatastore(data_dir))
    ReportService.initialize(container.resolve(AWSService))

    return container


def _register_conventions(container: DIContainer, data_dir: Path):
    container.register_convention(Path, "data_dir", data_dir)
    container.register_convention(
        AgentConfiguration, "default_agent_configuration", DEFAULT_AGENT_CONFIGURATION
    )
    container.register_convention(
        AgentConfiguration,
        "default_ransomware_agent_configuration",
        DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
    )


def _register_repositories(container: DIContainer, data_dir: Path):
    container.register_instance(
        IFileRepository,
        _decorate_file_repository(LocalStorageFileRepository(data_dir / "runtime_data")),
    )
    container.register_instance(IAgentBinaryRepository, _build_agent_binary_repository())
    container.register_instance(
        IAgentConfigurationRepository, container.resolve(FileAgentConfigurationRepository)
    )
    container.register_instance(ISimulationRepository, container.resolve(FileSimulationRepository))
    container.register_instance(
        ICredentialsRepository, container.resolve(MongoCredentialsRepository)
    )


def _decorate_file_repository(file_repository: IFileRepository) -> IFileRepository:
    return FileRepositoryLockingDecorator(
        FileRepositoryLoggingDecorator(FileRepositoryCachingDecorator(file_repository))
    )


def _build_agent_binary_repository():
    file_repository = _decorate_file_repository(LocalStorageFileRepository(AGENT_BINARIES_PATH))
    agent_binary_repository = AgentBinaryRepository(file_repository)

    _log_agent_binary_hashes(agent_binary_repository)

    return agent_binary_repository


def _log_agent_binary_hashes(agent_binary_repository: IAgentBinaryRepository):
    """
    Logs all the hashes of the agent executables for debbuging ease

    :param agent_binary_repository: Used to retrieve the agent binaries
    """
    agent_binaries = {
        "Linux": agent_binary_repository.get_linux_binary,
        "Windows": agent_binary_repository.get_windows_binary,
    }
    agent_hashes = {}

    for os, get_agent_binary in agent_binaries.items():
        try:
            agent_binary = get_agent_binary()
            binary_sha256_hash = get_binary_io_sha256_hash(agent_binary)
            agent_hashes[os] = binary_sha256_hash
        except RetrievalError as err:
            logger.error(f"No agent available for {os}: {err}")

    for os, binary_sha256_hash in agent_hashes.items():
        logger.info(f"{os} agent: SHA-256 hash: {binary_sha256_hash}")


def _register_services(container: DIContainer):
    container.register_instance(AWSService, container.resolve(AWSService))
    container.register_instance(LocalMonkeyRunService, container.resolve(LocalMonkeyRunService))
    container.register_instance(IslandModeService, container.resolve(IslandModeService))
