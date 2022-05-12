from pathlib import Path

from common import DIContainer
from common.aws import AWSInstance
from monkey_island.cc.services import AWSService, DirectoryFileStorageService, IFileStorageService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService

from . import AuthenticationService, JsonFileUserDatastore
from .reporting.report import ReportService


def initialize_services(data_dir: Path) -> DIContainer:
    container = DIContainer()
    container.register_instance(AWSInstance, AWSInstance())

    container.register_instance(
        IFileStorageService, DirectoryFileStorageService(data_dir / "custom_pbas")
    )
    container.register_instance(AWSService, container.resolve(AWSService))

    # This is temporary until we get DI all worked out.
    PostBreachFilesService.initialize(container.resolve(IFileStorageService))
    LocalMonkeyRunService.initialize(data_dir)
    AuthenticationService.initialize(data_dir, JsonFileUserDatastore(data_dir))
    ReportService.initialize(container.resolve(AWSService))

    return container
