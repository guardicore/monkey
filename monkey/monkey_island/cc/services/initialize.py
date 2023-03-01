import logging
import threading
from pathlib import Path

from pubsub.core import Publisher
from pymongo import MongoClient

from common import DIContainer
from common.agent_configuration import (
    DEFAULT_AGENT_CONFIGURATION,
    DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
    AgentConfiguration,
)
from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    register_common_agent_event_serializers,
)
from common.agent_events import AgentEventRegistry, register_common_agent_events
from common.aws import AWSInstance
from common.event_queue import (
    IAgentEventQueue,
    LockingAgentEventQueueDecorator,
    PyPubSubAgentEventQueue,
)
from common.types.concurrency import BasicLock, RLock
from common.utils.file_utils import get_binary_io_sha256_hash
from monkey_island.cc.event_queue import (
    IIslandEventQueue,
    LockingIslandEventQueueDecorator,
    PyPubSubIslandEventQueue,
)
from monkey_island.cc.repositories import (
    AgentBinaryRepository,
    AgentConfigurationValidationDecorator,
    AgentMachineFacade,
    AgentPluginRepositoryCachingDecorator,
    AgentPluginRepositoryLoggingDecorator,
    FileAgentConfigurationRepository,
    FileAgentLogRepository,
    FileAgentPluginRepository,
    FileRepositoryCachingDecorator,
    FileRepositoryLockingDecorator,
    FileRepositoryLoggingDecorator,
    FileSimulationRepository,
    IAgentBinaryRepository,
    IAgentConfigurationRepository,
    IAgentEventRepository,
    IAgentLogRepository,
    IAgentPluginRepository,
    IAgentRepository,
    ICredentialsRepository,
    IFileRepository,
    IMachineRepository,
    INodeRepository,
    ISimulationRepository,
    IUserRepository,
    JSONFileUserRepository,
    LocalStorageFileRepository,
    MongoAgentEventRepository,
    MongoAgentRepository,
    MongoCredentialsRepository,
    MongoMachineRepository,
    MongoNodeRepository,
    NetworkModelUpdateFacade,
    RetrievalError,
    initialize_machine_repository,
)
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH, PLUGIN_DIR_NAME
from monkey_island.cc.server_utils.encryption import ILockableEncryptor, RepositoryEncryptor
from monkey_island.cc.services import (
    AgentConfigurationSchemaService,
    AgentSignalsService,
    AWSService,
    IAgentConfigurationService,
    build_agent_configuration_service,
)
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService
from monkey_island.cc.setup.mongo.mongo_setup import MONGO_URL

from ..repositories.utils import AgentConfigurationSchemaCompiler
from . import AuthenticationService
from .reporting.report import ReportService

logger = logging.getLogger(__name__)

AGENT_BINARIES_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries"
REPOSITORY_KEY_FILE_NAME = "repository_key.bin"


def initialize_services(container: DIContainer, data_dir: Path):
    _register_conventions(container)

    container.register_instance(AWSInstance, AWSInstance())
    container.register_instance(MongoClient, MongoClient(MONGO_URL, serverSelectionTimeoutMS=100))
    container.register_instance(
        ILockableEncryptor, RepositoryEncryptor(data_dir / REPOSITORY_KEY_FILE_NAME)
    )
    container.register(Publisher, Publisher)
    _register_event_queues(container)

    _setup_agent_event_registry(container)
    _setup_agent_event_serializers(container)
    _register_repositories(container, data_dir)
    _register_services(container)

    # This is temporary until we get DI all worked out.
    ReportService.initialize(
        container.resolve(IAgentRepository),
        container.resolve(IAgentConfigurationRepository),
        container.resolve(IAgentEventRepository),
        container.resolve(IMachineRepository),
        container.resolve(INodeRepository),
        container.resolve(IAgentPluginRepository),
    )


def _register_conventions(container: DIContainer):
    container.register_convention(
        AgentConfiguration, "default_agent_configuration", DEFAULT_AGENT_CONFIGURATION
    )
    container.register_convention(
        AgentConfiguration,
        "default_ransomware_agent_configuration",
        DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
    )


def _register_event_queues(container: DIContainer):
    event_queue_lock = threading.RLock()

    agent_event_queue = container.resolve(PyPubSubAgentEventQueue)
    decorated_agent_event_queue = _decorate_agent_event_queue(agent_event_queue, event_queue_lock)
    container.register_instance(IAgentEventQueue, decorated_agent_event_queue)

    island_event_queue = container.resolve(PyPubSubIslandEventQueue)
    decorated_island_event_queue = _decorate_island_event_queue(
        island_event_queue, event_queue_lock
    )
    container.register_instance(IIslandEventQueue, decorated_island_event_queue)


def _decorate_agent_event_queue(
    agent_event_queue: IAgentEventQueue, lock: BasicLock
) -> IAgentEventQueue:
    return LockingAgentEventQueueDecorator(agent_event_queue, lock)


def _decorate_island_event_queue(
    island_event_queue: IIslandEventQueue, lock: RLock
) -> IIslandEventQueue:
    return LockingIslandEventQueueDecorator(island_event_queue, lock)


def _register_repositories(container: DIContainer, data_dir: Path):
    container.register_instance(
        IFileRepository,
        _decorate_file_repository(LocalStorageFileRepository(data_dir / "runtime_data")),
    )
    container.register_convention(
        IFileRepository,
        "plugin_file_repository",
        FileRepositoryLockingDecorator(
            FileRepositoryLoggingDecorator(LocalStorageFileRepository(data_dir / PLUGIN_DIR_NAME))
        ),
    )
    container.register_instance(IAgentBinaryRepository, _build_agent_binary_repository())

    container.register_instance(ISimulationRepository, container.resolve(FileSimulationRepository))
    container.register_instance(
        ICredentialsRepository, container.resolve(MongoCredentialsRepository)
    )
    container.register_instance(IUserRepository, container.resolve(JSONFileUserRepository))
    container.register_instance(IAgentEventRepository, container.resolve(MongoAgentEventRepository))

    container.register_instance(INodeRepository, container.resolve(MongoNodeRepository))
    container.register_instance(IMachineRepository, _build_machine_repository(container))
    container.register_instance(IAgentRepository, container.resolve(MongoAgentRepository))
    container.register_instance(IAgentLogRepository, container.resolve(FileAgentLogRepository))
    container.register_instance(AgentMachineFacade, container.resolve(AgentMachineFacade))
    container.register_instance(
        NetworkModelUpdateFacade, container.resolve(NetworkModelUpdateFacade)
    )
    container.register_instance(
        IAgentPluginRepository,
        _decorate_agent_plugin_repository(container.resolve(FileAgentPluginRepository)),
    )
    container.register_instance(
        AgentConfigurationSchemaCompiler, container.resolve(AgentConfigurationSchemaCompiler)
    )
    container.register_instance(
        IAgentConfigurationRepository, _build_file_agent_configuration_repository(container)
    )


def _decorate_file_repository(file_repository: IFileRepository) -> IFileRepository:
    return FileRepositoryLockingDecorator(
        FileRepositoryLoggingDecorator(FileRepositoryCachingDecorator(file_repository))
    )


def _decorate_agent_configuration_repository(
    agent_configuration_repository: IAgentConfigurationRepository,
    agent_configuration_schema_compiler: AgentConfigurationSchemaCompiler,
) -> IAgentConfigurationRepository:

    return AgentConfigurationValidationDecorator(
        agent_configuration_repository, agent_configuration_schema_compiler
    )


def _build_file_agent_configuration_repository(container: DIContainer):
    file_agent_configuration_repository = container.resolve(FileAgentConfigurationRepository)
    agent_configuration_schema_compiler = container.resolve(AgentConfigurationSchemaCompiler)
    return _decorate_agent_configuration_repository(
        file_agent_configuration_repository, agent_configuration_schema_compiler
    )


def _build_agent_binary_repository() -> IAgentBinaryRepository:
    file_repository = _decorate_file_repository(LocalStorageFileRepository(AGENT_BINARIES_PATH))
    agent_binary_repository = AgentBinaryRepository(file_repository)

    _log_agent_binary_hashes(agent_binary_repository)

    return agent_binary_repository


def _build_machine_repository(container: DIContainer) -> IMachineRepository:
    machine_repository = container.resolve(MongoMachineRepository)
    initialize_machine_repository(machine_repository)

    return machine_repository


def _decorate_agent_plugin_repository(
    plugin_repository: IAgentPluginRepository,
) -> IAgentPluginRepository:
    return AgentPluginRepositoryLoggingDecorator(
        AgentPluginRepositoryCachingDecorator(plugin_repository)
    )


def _setup_agent_event_registry(container: DIContainer):
    agent_event_registry = AgentEventRegistry()
    register_common_agent_events(agent_event_registry)

    container.register_instance(AgentEventRegistry, agent_event_registry)


def _setup_agent_event_serializers(container: DIContainer):
    agent_event_serializer_registry = AgentEventSerializerRegistry()
    register_common_agent_event_serializers(agent_event_serializer_registry)

    container.register_instance(AgentEventSerializerRegistry, agent_event_serializer_registry)


def _log_agent_binary_hashes(agent_binary_repository: IAgentBinaryRepository):
    """
    Logs all the hashes of the agent executables for debugging ease

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
    container.register_instance(AuthenticationService, container.resolve(AuthenticationService))
    container.register_instance(AgentSignalsService, container.resolve(AgentSignalsService))
    container.register_instance(
        AgentConfigurationSchemaService, container.resolve(AgentConfigurationSchemaService)
    )
    container.register_instance(
        IAgentConfigurationService, build_agent_configuration_service(container)
    )
