import logging
import threading
from pathlib import Path

from monkeytypes import BasicLock, RLock
from ophidian import DIContainer
from pubsub.core import Publisher
from pymongo import MongoClient

from common.agent_configuration import DEFAULT_AGENT_CONFIGURATION, AgentConfiguration
from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    register_common_agent_event_serializers,
)
from common.agent_events import AgentEventRegistry, register_common_agent_events
from common.event_queue import (
    IAgentEventQueue,
    LockingAgentEventQueueDecorator,
    PyPubSubAgentEventQueue,
)
from monkey_island.cc.event_queue import (
    IIslandEventQueue,
    LockingIslandEventQueueDecorator,
    PyPubSubIslandEventQueue,
)
from monkey_island.cc.repositories import (
    AgentMachineFacade,
    FileRepositoryCachingDecorator,
    FileRepositoryLockingDecorator,
    FileRepositoryLoggingDecorator,
    FileSimulationRepository,
    IAgentEventRepository,
    IAgentRepository,
    ICredentialsRepository,
    IFileRepository,
    IMachineRepository,
    INodeRepository,
    ISimulationRepository,
    LocalStorageFileRepository,
    MongoAgentEventRepository,
    MongoAgentRepository,
    MongoCredentialsRepository,
    MongoMachineRepository,
    MongoNodeRepository,
    NetworkModelUpdateFacade,
    initialize_machine_repository,
)
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.server_utils.encryption import ILockableEncryptor, RepositoryEncryptor
from monkey_island.cc.services import (
    AgentSignalsService,
    AWSService,
    IAgentBinaryService,
    IAgentConfigurationService,
    IAgentPluginService,
    build_agent_binary_service,
    build_agent_configuration_service,
    build_agent_plugin_service,
    build_aws_service,
)
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService
from monkey_island.cc.setup.mongo.mongo_setup import MONGO_URL

from .reporting.report import ReportService

logger = logging.getLogger(__name__)

AGENT_BINARIES_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries"
REPOSITORY_KEY_FILE_NAME = "repository_key.bin"


def initialize_services(container: DIContainer, data_dir: Path):
    _register_conventions(container)

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
        container.resolve(IAgentConfigurationService),
        container.resolve(IAgentEventRepository),
        container.resolve(IMachineRepository),
        container.resolve(INodeRepository),
        container.resolve(IAgentPluginService),
    )


def _register_conventions(container: DIContainer):
    container.register_convention(
        AgentConfiguration, "default_agent_configuration", DEFAULT_AGENT_CONFIGURATION
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

    container.register_instance(ISimulationRepository, container.resolve(FileSimulationRepository))
    container.register_instance(
        ICredentialsRepository, container.resolve(MongoCredentialsRepository)
    )
    container.register_instance(IAgentEventRepository, container.resolve(MongoAgentEventRepository))

    container.register_instance(INodeRepository, container.resolve(MongoNodeRepository))
    container.register_instance(IMachineRepository, _build_machine_repository(container))
    container.register_instance(IAgentRepository, container.resolve(MongoAgentRepository))
    container.register_instance(AgentMachineFacade, container.resolve(AgentMachineFacade))
    container.register_instance(
        NetworkModelUpdateFacade, container.resolve(NetworkModelUpdateFacade)
    )


def _decorate_file_repository(file_repository: IFileRepository) -> IFileRepository:
    return FileRepositoryLockingDecorator(
        FileRepositoryLoggingDecorator(FileRepositoryCachingDecorator(file_repository))
    )


def _build_machine_repository(container: DIContainer) -> IMachineRepository:
    machine_repository = container.resolve(MongoMachineRepository)
    initialize_machine_repository(machine_repository)

    return machine_repository


def _setup_agent_event_registry(container: DIContainer):
    agent_event_registry = AgentEventRegistry()
    register_common_agent_events(agent_event_registry)

    container.register_instance(AgentEventRegistry, agent_event_registry)


def _setup_agent_event_serializers(container: DIContainer):
    agent_event_serializer_registry = AgentEventSerializerRegistry()
    register_common_agent_event_serializers(agent_event_serializer_registry)

    container.register_instance(AgentEventSerializerRegistry, agent_event_serializer_registry)


def _register_services(container: DIContainer):
    container.register_instance(AWSService, build_aws_service(container))
    container.register_instance(AgentSignalsService, container.resolve(AgentSignalsService))
    container.register_instance(IAgentBinaryService, build_agent_binary_service(container))
    container.register_instance(IAgentPluginService, build_agent_plugin_service(container))
    container.register_instance(
        IAgentConfigurationService, build_agent_configuration_service(container)
    )
    container.register_instance(LocalMonkeyRunService, container.resolve(LocalMonkeyRunService))
