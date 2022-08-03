import json
import logging
from pathlib import Path

from pymongo import MongoClient

from common import DIContainer
from common.agent_configuration import (
    DEFAULT_AGENT_CONFIGURATION,
    DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
    AgentConfiguration,
)
from common.aws import AWSInstance
from common.common_consts.telem_categories import TelemCategoryEnum
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
    IUserRepository,
    JSONFileUserRepository,
    LocalStorageFileRepository,
    MongoCredentialsRepository,
    RetrievalError,
)
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.server_utils.encryption import ILockableEncryptor, RepositoryEncryptor
from monkey_island.cc.server_utils.island_logger import get_log_file_path
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.services import AWSService, IslandModeService, RepositoryService
from monkey_island.cc.services.attack.technique_reports.T1003 import T1003, T1003GetReportData
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService
from monkey_island.cc.services.telemetry.processing.credentials.credentials_parser import (
    CredentialsParser,
)
from monkey_island.cc.services.telemetry.processing.processing import (
    TELEMETRY_CATEGORY_TO_PROCESSING_FUNC,
)
from monkey_island.cc.setup.mongo.mongo_setup import MONGO_URL

from . import AuthenticationService
from .reporting.report import ReportService

logger = logging.getLogger(__name__)

AGENT_BINARIES_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries"
DEPLOYMENT_FILE_PATH = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "deployment.json"
REPOSITORY_KEY_FILE_NAME = "repository_key.bin"


def initialize_services(data_dir: Path) -> DIContainer:
    container = DIContainer()
    _register_conventions(container, data_dir)

    container.register_instance(AWSInstance, AWSInstance())
    container.register_instance(MongoClient, MongoClient(MONGO_URL, serverSelectionTimeoutMS=100))
    container.register_instance(
        ILockableEncryptor, RepositoryEncryptor(data_dir / REPOSITORY_KEY_FILE_NAME)
    )

    _register_repositories(container, data_dir)
    _register_services(container)

    _dirty_hacks(container)

    # This is temporary until we get DI all worked out.
    ReportService.initialize(
        container.resolve(AWSService),
        container.resolve(IAgentConfigurationRepository),
        container.resolve(ICredentialsRepository),
    )

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
    container.register_convention(Path, "island_log_file_path", get_log_file_path(data_dir))
    container.register_convention(Deployment, "deployment", _get_depyloyment_from_file(DEPLOYMENT_FILE_PATH))


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
    container.register_instance(IUserRepository, container.resolve(JSONFileUserRepository))


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

def _get_depyloyment_from_file(file_path: Path) -> Deployment:
    try:
        with open(file_path, "r") as deployment_info_file:
            deployment_info = json.load(deployment_info_file)
            return Deployment[deployment_info["deployment"].upper()]
    except FileNotFoundError as ex:
        logger.debug(f"Deployment file {file_path} is not found. Exception: {ex}")
    except KeyError as ex:
        logger.debug(f"Invalid key in the deployment file. Exception: {ex}")
    except json.JSONDecodeError as ex:
        logger.debug(f"Invalid deployment info file. Exception: {ex}")
    except Exception as ex:
        logger.debug(f"Couldn't get deployment info from {file_path}. Exception: {ex}.")


def _register_services(container: DIContainer):
    container.register_instance(AWSService, container.resolve(AWSService))
    container.register_instance(LocalMonkeyRunService, container.resolve(LocalMonkeyRunService))
    container.register_instance(IslandModeService, container.resolve(IslandModeService))
    container.register_instance(AuthenticationService, container.resolve(AuthenticationService))
    container.register_instance(RepositoryService, container.resolve(RepositoryService))


def _dirty_hacks(container: DIContainer):
    # A dirty hacks function that patches some of the things that
    # are needed at the current point

    # Patches attack technique T1003 which is a static class
    # but it needs stolen credentials from the database
    T1003.get_report_data = container.resolve(T1003GetReportData)

    # Note: A hack to resolve credentials parser
    # It changes telemetry processing function, this will be refactored!
    TELEMETRY_CATEGORY_TO_PROCESSING_FUNC[TelemCategoryEnum.CREDENTIALS] = container.resolve(
        CredentialsParser
    )
